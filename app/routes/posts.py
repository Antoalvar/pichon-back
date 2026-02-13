from flask import Blueprint, request, jsonify
from app.services.posts_service import PostsService

posts_bp = Blueprint('posts', __name__, url_prefix='/create_post')


@posts_bp.route('', methods=['GET'])
def get_posts():
    """
    Obtiene todos los registros de la tabla index en PostgreSQL.
    """
    try:
        data = PostsService.get_all_index()
        return jsonify({
            "status": "success",
            "data": data,
            "count": len(data)
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@posts_bp.route('', methods=['POST'])
def create_post():
    """
    Crea un nuevo post (artículo) en la base de datos.
    Recibe: title, abstract, img, categories, prod, body
    """
    if not request.is_json:
        return jsonify({"message": "Falta el body en formato JSON"}), 400

    data = request.get_json()
    required_fields = ["title", "abstract", "img", "categories", "prod", "body"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"El campo '{field}' es obligatorio"}), 400

    try:
        post_id = PostsService.create_post(
            title=data['title'],
            abstract=data['abstract'],
            img=data['img'],
            categories=data['categories'],
            prod=data['prod'],
            body=data['body']
        )
        return jsonify({
            "status": "success",
            "message": "Post creado correctamente",
            "id": post_id
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
