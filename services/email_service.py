# services/email_service.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.email = os.getenv('EMAIL_USERNAME')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def get_template_cadastro(self, nome, email, senha):
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                <div style="text-align: center; padding: 20px;">
                    <h1 style="color: #4CAF50; margin: 0;">Estamos quase lá!</h1>
                </div>
                
                <div style="padding: 20px; background-color: #f9f9f9; border-radius: 5px;">
                    <p>Olá, <strong>{nome}</strong>!</p>
                    
                    <p>Seu cadastro no sistema de Redação do ENEM 2024 foi realizado com sucesso!</p>
                    
                    <p>Suas credenciais de acesso são:</p>
                    <div style="background-color: #ffffff; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p style="margin: 5px 0;"><strong>Email:</strong> {email}</p>
                        <p style="margin: 5px 0;"><strong>Senha:</strong> {senha}</p>
                    </div>
                    
                    <p>Para acessar o sistema, clique no botão abaixo:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:5000/login" 
                           style="background-color: #4CAF50; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                            Acessar o Sistema
                        </a>
                    </div>
                    
                    <p style="font-size: 0.9em; color: #666;">
                        Por favor, mantenha suas credenciais em segurança e não as compartilhe com ninguém.
                    </p>
                </div>
                
                <div style="text-align: center; margin-top: 20px; color: #666; font-size: 0.8em;">
                    <p>Este é um email automático, por favor não responda.</p>
                </div>
            </div>
        </body>
        </html>
        """

    def enviar_email_cadastro(self, nome, email, senha):
        try:
            # Configurar a mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Bem-vindo ao Sistema de Redação ENEM 2024"
            msg['From'] = self.email
            msg['To'] = email

            # Criar o corpo do email em HTML
            html = self.get_template_cadastro(nome, email, senha)
            msg.attach(MIMEText(html, 'html'))

            # Conectar ao servidor SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)

            # Enviar email
            server.send_message(msg)
            server.quit()

            print(f"Email enviado com sucesso para {email}")
            return True, "Email enviado com sucesso"

        except Exception as e:
            print(f"Erro ao enviar email: {str(e)}")
            return False, f"Erro ao enviar email: {str(e)}"
        
    def enviar_email_recuperacao(self, nome, email, nova_senha):
        try:
            # Configurar a mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Recuperação de Senha - Redação ENEM 2024"
            msg['From'] = self.email
            msg['To'] = email

            # Criar o corpo do email em HTML
            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                    <h1 style="color: #4CAF50; text-align: center;">Nova Senha Gerada</h1>
                    
                    <p>Olá, <strong>{nome}</strong>!</p>
                    
                    <p>Uma nova senha foi gerada para sua conta:</p>
                    
                    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center;">
                        <p style="font-size: 24px; margin: 0;"><strong>{nova_senha}</strong></p>
                    </div>
                    
                    <p>Use esta senha para acessar sua conta. Recomendamos que você troque esta senha após o primeiro acesso.</p>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="http://localhost:5000/login" 
                        style="background-color: #4CAF50; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px;">
                            Acessar o Sistema
                        </a>
                    </div>
                </div>
            </body>
            </html>
            """
        
            msg.attach(MIMEText(html, 'html'))

            # Enviar email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()

            return True, "Email enviado com sucesso"

        except Exception as e:
            return False, f"Erro ao enviar email: {str(e)}"