from config.firebase_config import FirebaseConfig
import datetime
import os

def test_firebase_connection():
    try:
        print("Verificando ambiente...")
        # Verifica o diretório atual
        print(f"Diretório atual: {os.getcwd()}")
        
        # Verifica se o arquivo de credenciais existe
        cred_path = os.path.join('config', 'firebase_credentials.json')
        if os.path.exists(cred_path):
            print(f"✓ Arquivo de credenciais encontrado em: {cred_path}")
        else:
            print(f"❌ Arquivo de credenciais não encontrado em: {cred_path}")
            return False

        print("\nIniciando conexão com Firebase...")
        firebase = FirebaseConfig()
        db = firebase.get_db()
        
        # Dados de teste
        test_user = {
            'nome': 'Usuário Teste',
            'email': 'teste@teste.com',
            'data_teste': datetime.datetime.now(),
        }
        
        print("✓ Conexão estabelecida")
        
        # Tenta adicionar um documento
        doc_ref = db.collection('teste').document()
        doc_ref.set(test_user)
        print("✓ Documento criado com sucesso!")
        
        # Tenta ler o documento
        doc = doc_ref.get()
        if doc.exists:
            print("✓ Documento lido com sucesso!")
            print("Dados do documento:", doc.to_dict())
        
        # Tenta deletar o documento de teste
        doc_ref.delete()
        print("✓ Documento de teste removido!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {str(e)}")
        print(f"Tipo do erro: {type(e)}")
        return False

if __name__ == "__main__":
    test_firebase_connection()