from flask import Blueprint, request, jsonify
from app.services.pichon_db_service import IndexService

index_bp = Blueprint('index', __name__, url_prefix='/index')


@index_bp.route('', methods=['GET'])
def get_index():
    """
    Obtiene todos los registros de la tabla index en PostgreSQL.
    """
    try:
        data = IndexService.get_all_indexes()
        return jsonify({
            "status": "success",
            "data": data,
            "count": len(data)
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@index_bp.route('', methods=['POST'])
def add_index():
    """
    Crea un nuevo registro en la tabla index.
    Recibe: id (opcional), img, title, abstract, categories, prod
    """

    # 1. Verificar que la petición contenga datos JSON
    if not request.is_json:
        return jsonify({"message": "Falta el body en formato JSON"}), 400

    data = request.get_json()

    # 2. Validar campos requeridos
    required_fields = ["img", "title", "abstract", "categories", "prod"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"El campo '{field}' es obligatorio"}), 400

    try:
        # 3. Crear el índice usando el servicio
        entry_id = IndexService.create_index(
            img=data['img'],
            title=data['title'],
            abstract=data['abstract'],
            categories=data['categories'],
            prod=data['prod'],
            entry_id=data.get('id')
        )

        return jsonify({
            "status": "success",
            "message": "Registro agregado correctamente",
            "id": entry_id
        }), 201

    except Exception as e:
        error_message = str(e)
        status_code = 409 if "ya existe" in error_message else 500
        return jsonify({"status": "error", "message": error_message}), status_code
