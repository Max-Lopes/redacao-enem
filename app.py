from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from crewai import Crew
from agents.text_reviewer import EnemAgents
from tasks.review_tasks import ReviewTasks
from config.theme_manager import ThemeManager
from config.llm_config import LLMConfig
from dotenv import load_dotenv
from services.user_service import UserService
from functools import wraps
import json
import traceback
import re
import os
from datetime import timedelta


# Inicialização do Flask
app = Flask(__name__)
load_dotenv()

app.secret_key = os.getenv('SECRET_KEY', 'chave-temporaria-de-backup')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

user_service = UserService()

# A rota principal redireciona para login
@app.route('/')
def index():
    if 'user_email' in session:
        return redirect(url_for('sistema'))
    return redirect(url_for('login'))

# Configurar a secret_key para a sessão
app.secret_key = os.getenv('SECRET_KEY', 'uma-chave-secreta-temporaria')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        lembrar = request.form.get('lembrar') == 'on'  # Verificar se checkbox está marcado
        
        sucesso, resultado = user_service.validar_login(email, senha)
        
        if sucesso:
            # Configurar a sessão
            session['user_email'] = email
            session['user_nome'] = resultado['nome']
            
            if lembrar:
                # Se "Lembrar de mim" estiver marcado, define tempo de duração da sessão
                session.permanent = True
                # 30 dias de duração do cookie
                app.permanent_session_lifetime = timedelta(days=30)
            else:
                session.permanent = False
                
            return jsonify({'success': True})
        else:
            return jsonify({'error': resultado}), 401
            
    return render_template('login.html')

@app.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            return jsonify({'error': 'Email é obrigatório'}), 400
            
        sucesso, msg = user_service.recuperar_senha(email)
        
        if sucesso:
            return jsonify({'message': msg})
        else:
            return jsonify({'error': msg}), 400
            
    return render_template('recuperar_senha.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Proteger a rota do sistema
@app.route('/sistema')
@login_required
def sistema():
    return render_template('index.html', user_email=session.get('user_email'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()
        idade = request.form.get('idade', 0)
        estado = request.form.get('estado', '').strip()

        # Validações usando o UserService
        user_service = UserService()
        
        # Validar email
        email_valido, msg_email = user_service.validar_email(email)
        if not email_valido:
            return jsonify({'error': msg_email}), 400

        # Validar telefone
        tel_valido, msg_tel = user_service.validar_telefone(telefone)
        if not tel_valido:
            return jsonify({'error': msg_tel}), 400

        # Validar idade
        try:
            idade = int(idade)
            if idade < 13 or idade > 100:
                return jsonify({'error': 'Idade deve estar entre 13 e 100 anos'}), 400
        except:
            return jsonify({'error': 'Idade inválida'}), 400

        # Validar estado
        estados_validos = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
                          'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
                          'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
        if estado not in estados_validos:
            return jsonify({'error': 'Estado inválido'}), 400

        # Se chegou aqui, dados são válidos
        dados = {
            'nome': nome,
            'email': email,
            'telefone': telefone,
            'idade': idade,
            'estado': estado
        }
        
        sucesso, resultado = user_service.criar_usuario(dados)
        
        if sucesso:
            return jsonify({
                'message': 'Cadastro realizado com sucesso',
                'senha': resultado['senha']
            }), 200
        else:
            return jsonify({'error': resultado}), 400

    return render_template('cadastro.html')


@app.route('/get-themes', methods=['GET'])
def get_themes():
    return jsonify(ThemeManager.DEFAULT_THEMES)

@app.route('/analyze', methods=['POST'])
@login_required  # Proteger esta rota também
def analyze():
    try:
        print("\n=== DEBUG /analyze ===")
        print("Form data recebido:", dict(request.form))
        print("===================\n")

        # Obter e validar o texto
        texto = request.form.get('texto', '').strip()
        if not texto:
            return render_template('error.html', 
                error="O texto não pode estar vazio.")
        
        if len(texto) > 5000:
            return render_template('error.html', 
                error="O texto é muito longo. Por favor, limite a 5000 caracteres.")

        # Processar o tema
        try:
            tema = ThemeManager.process_theme_request(request.form)
        except ValueError as e:
            return render_template('error.html', error=str(e))
        
        # Criar os agentes
        enem_agents = EnemAgents()
        agents = enem_agents.create_agents()
        
        # Criar as tarefas
        tasks = ReviewTasks.create_review_tasks(agents, texto, tema)
        
        # Criar e executar a crew
        crew = Crew(
            tasks=tasks,
            verbose=True
        )
        
        # Executar as avaliações
        print("\nIniciando execução da crew:")
        resultados = crew.kickoff()
        print("Execução da crew concluída")
        
        # Processar resultados
        resultados_processados = processar_resultados(resultados)
        
        # Verificar se obtivemos algum resultado
        if all(nota == 0 for nota in resultados_processados['notas_individuais']):
            print("AVISO: Nenhuma nota foi processada com sucesso")
        
        return render_template('result.html', 
                             user_email=session.get('user_email'),
                             **resultados_processados)
    except Exception as e:
        print("Erro durante a análise:")
        traceback.print_exc()
        return render_template('error.html', error=str(e))

def processar_resultados(resultados):
    """Função para processar os resultados usando tasks_output"""
    num_competencias = 5
    notas = [0] * num_competencias
    feedback = ["Não avaliado"] * num_competencias
    problemas = [[] for _ in range(num_competencias)]
    sugestoes = [[] for _ in range(num_competencias)]

    print("\nProcessando resultados das tarefas:")
    
    # Acessar as tarefas individuais
    if hasattr(resultados, 'tasks_output'):
        tasks = resultados.tasks_output
        print(f"Número de tarefas encontradas: {len(tasks)}")
        
        for i, task in enumerate(tasks):
            if i < num_competencias:
                try:
                    # Extrair o resultado da tarefa
                    resultado_str = task.raw if hasattr(task, 'raw') else str(task)
                    print(f"\nProcessando tarefa {i+1}:")
                    print(f"Conteúdo: {resultado_str[:100]}...")  # Primeiros 100 caracteres
                    
                    # Converter para JSON
                    analise = json.loads(resultado_str)
                    
                    # Guardar os resultados
                    notas[i] = float(analise['nota'])
                    feedback[i] = str(analise['justificativa'])
                    problemas[i] = analise.get('problemas', [])
                    sugestoes[i] = analise.get('sugestoes', [])
                    
                    print(f"Tarefa {i+1} processada: Nota = {notas[i]}")
                    
                except Exception as e:
                    print(f"Erro ao processar tarefa {i+1}: {e}")
                    print(f"Resultado problemático: {resultado_str}")
                    continue
    else:
        print("Aviso: Objeto não tem tasks_output, tentando processar raw")
        try:
            # Tentar processar o resultado raw
            if hasattr(resultados, 'raw'):
                analise = json.loads(resultados.raw)
                notas[0] = float(analise['nota'])
                feedback[0] = str(analise['justificativa'])
                problemas[0] = analise.get('problemas', [])
                sugestoes[0] = analise.get('sugestoes', [])
                print("Processado resultado raw com sucesso")
        except Exception as e:
            print(f"Erro ao processar resultado raw: {e}")
    
    print("\nResultados finais:")
    for i in range(num_competencias):
        print(f"Competência {i+1}: Nota {notas[i]}")
    
    return {
        'nota_final': sum(notas),
        'notas_individuais': notas,
        'feedback': feedback,
        'problemas': problemas,
        'sugestoes': sugestoes
    }




if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)