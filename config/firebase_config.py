import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import json

class FirebaseConfig:
    def __init__(self):
        try:
            # Obtém o caminho absoluto para o arquivo de credenciais
            current_dir = os.path.dirname(os.path.abspath(__file__))
            cred_path = os.path.join(current_dir, 'firebase_credentials.json')
            
            # Verifica se o arquivo existe
            if not os.path.exists(cred_path):
                raise FileNotFoundError(f"Arquivo de credenciais não encontrado em: {cred_path}")
            
            # Tenta ler o arquivo para verificar se é um JSON válido
            with open(cred_path, 'r') as file:
                json.load(file)
            
            # Inicializa o Firebase Admin SDK
            cred = credentials.Certificate(cred_path)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            
            # Inicializa o Firestore
            self.db = firestore.client()
            self.auth = auth
            
        except FileNotFoundError as e:
            print(f"Erro: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            raise
        except Exception as e:
            print(f"Erro ao inicializar Firebase: {e}")
            raise

    def get_db(self):
        return self.db

    def get_auth(self):
        return self.auth