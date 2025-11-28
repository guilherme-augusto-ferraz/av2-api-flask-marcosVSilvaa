# app.py
from flask import Flask
from database import configure_database, db
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Importe o modelo User - Necessário para a correção do JWT
from models.user import User 

# 1. Carrega as variáveis de ambiente (.env)
load_dotenv()

# Inicialização da Aplicação
app = Flask(__name__)

# 2. Configuração do JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# =================================================================
# CORREÇÃO CRÍTICA: Configuração do JWT para lidar com IDs inteiros
# =================================================================

# 1. Define qual valor será armazenado no token (o ID do usuário)
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

# 2. Define como encontrar o usuário no banco de dados a partir do ID do token
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # 'sub' é onde o ID (subject) fica no token
    identity = jwt_data["sub"] 
    # Usa o ID para buscar o usuário no DB
    return User.query.filter_by(id=identity).one_or_none()

# =================================================================
# FIM DA CORREÇÃO
# =================================================================

# 3. Configuração e Inicialização do Banco de Dados
configure_database(app)

# 4. Importação e Registro das Rotas (Etapas 3 e 4)
from routes.users import users_bp
from routes.tasks import tasks_bp 

# REGISTRO FINAL DOS BLUEPRINTS:
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(tasks_bp, url_prefix='/api/tasks') 

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