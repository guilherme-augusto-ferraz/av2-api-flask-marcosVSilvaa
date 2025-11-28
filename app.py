# app.py
from flask import Flask
from database import configure_database, db # Importa db
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# 1. Carrega as variáveis de ambiente (.env)
load_dotenv()

# Inicialização da Aplicação
app = Flask(__name__)

# 2. Configuração do JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# 3. Configuração e Inicialização do Banco de Dados
configure_database(app)

# 4. Importação e Registro das Rotas (Etapas 3 e 4)
# Importa o Blueprint das rotas de usuário
from routes.users import users_bp 
# from routes.tasks import tasks_bp # Será usado na Etapa 4

# Registra o Blueprint das rotas de usuário.
app.register_blueprint(users_bp, url_prefix='/api/users')
# app.register_blueprint(tasks_bp, url_prefix='/api/tasks') # Será usado na Etapa 4

@app.route('/')
def hello_world():
    return 'API de Lista de Tarefas está online!'

if __name__ == '__main__':
    # Importa os modelos para que o SQLAlchemy saiba quais tabelas criar
    from models.user import User
    from models.task import Task 
    
    # Cria as tabelas no BD (users e tasks), se não existirem
    with app.app_context():
        db.create_all() 
    
    app.run(debug=True)