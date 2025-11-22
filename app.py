# app.py
from flask import Flask
from database import configure_database, db
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# 1. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicialização da Aplicação
app = Flask(__name__)

# 2. Configuração do JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# 3. Configuração e Inicialização do Banco de Dados
configure_database(app)

# 4. Importação e Registro das Rotas (faremos isso na próxima etapa)
# from routes.users import users_bp
# app.register_blueprint(users_bp, url_prefix='/api/users')
# ...

@app.route('/')
def hello_world():
    return 'API de Gerenciamento Financeiro está online!'

if __name__ == '__main__':
    # Importe os modelos aqui para garantir que o db.create_all() os encontre
    from models.user import User
    from models.registro import Transaction
    
    app.run(debug=True)