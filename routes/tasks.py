# routes/tasks.py
from flask import Blueprint, request, jsonify
from models.task import Task
from database import db
# Importa o decorador de proteção e a função para ler o ID do usuário do token
from flask_jwt_extended import jwt_required, get_jwt_identity 
from datetime import datetime

# Cria o Blueprint para as rotas de tarefas
tasks_bp = Blueprint('tasks', __name__)

# O decorador @jwt_required() garante que a requisição
# contenha um token JWT válido no cabeçalho Authorization.
# A função get_jwt_identity() extrai o user_id do token.

# --- 1. CREATE: Criação de uma nova Tarefa (POST /api/tasks) ---
@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    # Obtém o ID do usuário logado através do token
    user_id = get_jwt_identity() 
    data = request.get_json()

    # 1. Validação básica de campos obrigatórios
    if 'title' not in data or 'due_date' not in data:
        return jsonify({"msg": "Título e data de vencimento são obrigatórios"}), 400

    try:
        # Converte a string de data (esperada no formato YYYY-MM-DD) para o objeto Date do Python
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()

        # 2. Cria o objeto Task (Instanciação POO)
        new_task = Task(
            title=data['title'],
            description=data.get('description'),
            status=data.get('status', 'pendente'), # Define 'pendente' como padrão
            due_date=due_date,
            user_id=user_id # Requisito Obrigatório: Associa a tarefa ao usuário autenticado
        )
        
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"msg": "Tarefa criada com sucesso!", "id": new_task.id}), 201
        
    except ValueError:
        return jsonify({"msg": "Formato de data inválido. Use AAAA-MM-DD"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Erro interno ao criar tarefa", "error": str(e)}), 500

# --- 2. READ (Listagem): Lista TODAS as tarefas do usuário logado (GET /api/tasks) ---
@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def list_tasks():
    user_id = get_jwt_identity()
    
    # Consulta: Filtra APENAS as tarefas que pertencem a este user_id
    # Ordenamos pela data para facilitar a visualização por dia
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.due_date).all()
    
    # Serializa os objetos POO em JSON
    output = []
    for task in tasks:
        output.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'due_date': task.due_date.isoformat(), # Converte data para string no formato ISO
            'user_id': task.user_id
        })
        
    return jsonify(output), 200


# --- 3. READ (Individual): Busca uma tarefa específica (GET /api/tasks/<int:id>) ---
@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    
    # Consulta: Busca a tarefa pelo ID E garante que ela pertence ao usuário
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        # Se não encontrou ou a tarefa existe, mas pertence a outro usuário
        return jsonify({"msg": "Tarefa não encontrada ou acesso negado"}), 404

    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'due_date': task.due_date.isoformat(),
        'user_id': task.user_id
    }), 200

# --- 4. UPDATE: Atualização de uma Tarefa (PUT /api/tasks/<int:id>) ---
@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # 1. Encontra a tarefa (garantindo que pertença ao usuário)
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({"msg": "Tarefa não encontrada ou acesso negado"}), 404
        
    # 2. Atualiza os campos: usa o valor do JSON, senão mantém o valor atual
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    
    # Atualiza a data se for fornecida
    if 'due_date' in data:
        try:
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"msg": "Formato de data inválido. Use AAAA-MM-DD"}), 400

    db.session.commit()
    return jsonify({"msg": "Tarefa atualizada com sucesso!"}), 200


# --- 5. DELETE: Remoção de uma Tarefa (DELETE /api/tasks/<int:id>) ---
@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    
    # 1. Encontra a tarefa (garantindo que pertença ao usuário)
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({"msg": "Tarefa não encontrada ou acesso negado"}), 404

    # 2. Deleta a tarefa
    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": "Tarefa removida com sucesso!"}), 200