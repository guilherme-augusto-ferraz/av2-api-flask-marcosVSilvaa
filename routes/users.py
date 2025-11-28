# routes/users.py
from flask import Blueprint, request, jsonify
from models.user import User # Importa o modelo POO de usuário
from database import db
from flask_jwt_extended import create_access_token # Função para criar o token

# Cria o Blueprint para agrupar as rotas
users_bp = Blueprint('users', __name__)

# --- Rota 1: Cadastro (Registro de novo usuário) ---
@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validação de dados de entrada
    if not username or not email or not password:
        return jsonify({"msg": "Nome de usuário, email e senha são obrigatórios"}), 400

    # Verifica se o usuário ou email já existem
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"msg": "Nome de usuário ou email já registrado"}), 409

    # Cria o objeto User (Instanciação POO)
    new_user = User(username=username, email=email)
    
    # Usa o método da classe User (POO) para criptografar e salvar a senha
    new_user.set_password(password) 

    try:
        db.session.add(new_user)
        db.session.commit()
        # Retorna o status 201 Created (Criado)
        return jsonify({"msg": "Usuário registrado com sucesso!", "user_id": new_user.id}), 201 
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Erro ao registrar usuário", "error": str(e)}), 500


# --- Rota 2: Login (Autenticação e Geração de JWT) ---
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 1. Encontra o usuário pelo nome
    user = User.query.filter_by(username=username).first()

    # 2. Verifica se o usuário existe E se a senha está correta (usando o método POO)
    if user and user.check_password(password):
        
        # 3. Geração do Token JWT (JSON Web Token)
        # identity=user.id armazena o ID do usuário DENTRO do token para ser usado
        # para identificar o usuário em rotas protegidas (Etapa 4).
        access_token = create_access_token(identity=user)
        
        return jsonify({
            "msg": "Login bem-sucedido",
            "access_token": access_token # O token é o passaporte de acesso
        }), 200
        
    return jsonify({"msg": "Nome de usuário ou senha incorretos"}), 401