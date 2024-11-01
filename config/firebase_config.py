# config/firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import json

class FirebaseConfig:
    def __init__(self):
        try:
            # Tenta pegar as credenciais da variável de ambiente
            google_creds = os.getenv('GOOGLE_CREDENTIALS')
            
            if google_creds:
                # Converte a string JSON em dicionário
                creds_dict = json.loads(google_creds)
                cred = credentials.Certificate(creds_dict)
            else:
                # Fallback para arquivo local durante desenvolvimento
                current_dir = os.path.dirname(os.path.abspath(__file__))
                cred_path = os.path.join(current_dir, 'firebase_credentials.json')
                
                if not os.path.exists(cred_path):
                    raise FileNotFoundError(f"Credenciais do Firebase não encontradas")
                
                cred = credentials.Certificate(cred_path)

            # Inicializa o Firebase Admin SDK
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            
            # Inicializa o Firestore
            self.db = firestore.client()
            self.auth = auth
            
        except Exception as e:
            print(f"Erro ao inicializar Firebase: {str(e)}")
            raise

    def get_db(self):
        return self.db

    def get_auth(self):
        return self.auth