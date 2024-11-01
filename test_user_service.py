from services.user_service import UserService

def test_cadastro_login():
    user_service = UserService()
    
    # Dados de teste
    dados_teste = {
        'nome': 'Usuário Teste',
        'email': 'teste@teste.com',
        'telefone': '(11) 99999-9999',
        'idade': 25,
        'estado': 'SP'
    }
    
    print("\n=== Iniciando Testes ===")
    
    # Teste de validação de email
    print("\n1. Testando validação de email...")
    email_valido, msg_email = user_service.validar_email(dados_teste['email'])
    print(f"Resultado: {'✓ Email válido' if email_valido else f'❌ Erro: {msg_email}'}")
    
    # Teste de validação de telefone
    print("\n2. Testando validação de telefone...")
    tel_valido, msg_tel = user_service.validar_telefone(dados_teste['telefone'])
    print(f"Resultado: {'✓ Telefone válido' if tel_valido else f'❌ Erro: {msg_tel}'}")
    
    # Teste de criação de usuário
    print("\n3. Testando cadastro de usuário...")
    sucesso, resultado = user_service.criar_usuario(dados_teste)
    
    if sucesso:
        print("✓ Usuário criado com sucesso!")
        print(f"✓ Senha gerada: {resultado['senha']}")
        senha_gerada = resultado['senha']
        
        # Teste de login
        print("\n4. Testando login...")
        sucesso_login, resultado_login = user_service.validar_login(
            dados_teste['email'], 
            senha_gerada
        )
        
        if sucesso_login:
            print("✓ Login realizado com sucesso!")
            print(f"✓ Dados do usuário recuperados: {resultado_login['nome']}")
        else:
            print(f"❌ Erro no login: {resultado_login}")
    else:
        print(f"❌ Erro no cadastro: {resultado}")
    
    print("\n=== Fim dos Testes ===\n")

if __name__ == "__main__":
    test_cadastro_login()