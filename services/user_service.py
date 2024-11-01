from config.firebase_config import FirebaseConfig
from .email_service import EmailService
import random
import string
import re

class UserService:
    def __init__(self):
        firebase = FirebaseConfig()
        self.db = firebase.get_db()
        self.auth = firebase.get_auth()
        self.email_service = EmailService() 

    def gerar_senha(self, tamanho=6):
        return ''.join(random.choices(string.digits, k=tamanho))

    def validar_email(self, email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(padrao, email):
            return False, "Formato de email inválido"
        # Verifica no Firebase
        usuarios = self.db.collection('usuarios').where('email', '==', email).get()
        if len(usuarios) > 0:
            return False, "Email já cadastrado"
        return True, ""

    def validar_telefone(self, telefone):
        telefone = re.sub(r'\D', '', telefone)
        if len(telefone) != 11:
            return False, "Telefone deve ter 11 dígitos"
        return True, ""

    def criar_usuario(self, dados):
        try:
            # Validações (mantemos as mesmas que já existem)
            if not dados['nome'] or len(dados['nome']) < 3:
                return False, "Nome deve ter pelo menos 3 caracteres"

            email_valido, msg_email = self.validar_email(dados['email'])
            if not email_valido:
                return False, msg_email

            tel_valido, msg_tel = self.validar_telefone(dados['telefone'])
            if not tel_valido:
                return False, msg_tel

            try:
                idade = int(dados['idade'])
                if idade < 13 or idade > 100:
                    return False, "Idade deve estar entre 13 e 100 anos"
            except:
                return False, "Idade inválida"

            estados_validos = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
                             'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
                             'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
            if dados['estado'] not in estados_validos:
                return False, "Estado inválido"

            # Gera senha
            senha = self.gerar_senha()
            
            # Prepara dados para salvar
            novo_usuario = {
                'nome': dados['nome'],
                'email': dados['email'],
                'telefone': dados['telefone'],
                'idade': idade,
                'estado': dados['estado'],
                'senha': senha
            }
            
            # Salva no Firestore
            self.db.collection('usuarios').add(novo_usuario)

            # Envia email com as credenciais
            sucesso_email, msg_email = self.email_service.enviar_email_cadastro(
                dados['nome'],
                dados['email'],
                senha
            )
            
            if not sucesso_email:
                print(f"Aviso: {msg_email}")

            
            return True, {
                'message': 'Cadastro realizado com sucesso',
                'senha': senha
            }

        except Exception as e:
            return False, f"Erro ao criar usuário: {str(e)}"
        
    def recuperar_senha(self, email):
        try:
            # Busca o usuário pelo email
            usuarios = self.db.collection('usuarios').where('email', '==', email).get()
            usuarios_list = list(usuarios)
        
            if len(usuarios_list) == 0:
                return False, "Email não encontrado"
        
            # Gera nova senha
            nova_senha = self.gerar_senha()
        
            # Atualiza no Firebase
            user_doc = usuarios_list[0]
            user_ref = self.db.collection('usuarios').document(user_doc.id)
            user_ref.update({'senha': nova_senha})
        
            # Envia email com nova senha
            usuario = user_doc.to_dict()
            sucesso_email, msg_email = self.email_service.enviar_email_recuperacao(
                usuario['nome'],
                email,
                nova_senha
            )
        
            if not sucesso_email:
                return False, "Erro ao enviar email de recuperação"
            
            return True, "Nova senha enviada para seu email"
        
        except Exception as e:
            return False, f"Erro ao recuperar senha: {str(e)}"
        
    def validar_login(self, email, senha):
        try:
            # Busca exata por email e senha
            query = self.db.collection('usuarios')\
                      .where('email', '==', email)\
                      .where('senha', '==', senha)\
                      .get()
        
            # Se encontrou exatamente um documento com email e senha corretos
            usuarios = list(query)
            if len(usuarios) == 1:
                return True, usuarios[0].to_dict()
        
            # Se não encontrou ou encontrou mais de um, login inválido
            return False, "Credenciais inválidas"
        
        except Exception as e:
            return False, "Erro na validação"

    def test_login_seguranca():
        user_service = UserService()
    
        # Criar dois usuários de teste
        usuario1 = {
            'nome': 'Teste 1',
            'email': 'teste1@teste.com',
            'telefone': '(11) 99999-9999',
            'idade': 25,
            'estado': 'SP'
         }
    
        usuario2 = {
            'nome': 'Teste 2',
            'email': 'teste2@teste.com',
            'telefone': '(11) 88888-8888',
            'idade': 30,
            'estado': 'RJ'
        }
    
        print("\n=== Teste de Segurança de Login ===")
    
        # Cadastrar usuários
        sucesso1, resultado1 = user_service.criar_usuario(usuario1)
        sucesso2, resultado2 = user_service.criar_usuario(usuario2)
    
        if sucesso1 and sucesso2:
            senha1 = resultado1['senha']
            senha2 = resultado2['senha']
        
            print("\nTentando login com email do usuário 1 e senha do usuário 2...")
            sucesso_login, _ = user_service.validar_login(usuario1['email'], senha2)
            print(f"Resultado: {'❌ Correto - Login negado' if not sucesso_login else '⚠️ ERRO - Login permitido incorretamente'}")
        
            print("\nTentando login correto usuário 1...")
            sucesso_login, _ = user_service.validar_login(usuario1['email'], senha1)
            print(f"Resultado: {'✓ Correto - Login permitido' if sucesso_login else '⚠️ ERRO - Login negado incorretamente'}")
        
            print("\nTentando múltiplas vezes com credenciais erradas...")
            for _ in range(5):
                sucesso_login, _ = user_service.validar_login(usuario1['email'], senha2)
                if sucesso_login:
                    print("⚠️ ERRO CRÍTICO - Login permitido após múltiplas tentativas!")
                    break
        
    print("\n=== Fim do Teste ===\n")

    if __name__ == "__main__":
        test_login_seguranca()



    