from flask import Blueprint, request, jsonify
from app.services.posts_service import PostsService

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')


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
    Recibe: title, abstract, img, categories, prod, content
    """
    if not request.is_json:
        return jsonify({"message": "Falta el content en formato JSON"}), 400

    data = request.get_json()
    required_fields = ["title", "abstract", "img", "categories", "prod", "content"]
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
            content=data['content']
        )
        return jsonify({
            "status": "success",
            "message": "Post creado correctamente",
            "id": post_id
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@posts_bp.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    """
    Obtiene un post específico por su ID.
    """
    try:
        post = PostsService.get_post_by_id(post_id)
        if post is None:
            return jsonify({"status": "error", "message": "Post no encontrado"}), 404
        return jsonify({"status": "success", "data": post}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@posts_bp.route('/<post_id>', methods=['PATCH'])
def update_post(post_id):
    """
    Actualiza parcialmente un post por su ID.
    Solo se actualizan los campos recibidos en el body.
    """
    if not request.is_json:
        return jsonify({"message": "Se requiere content en formato JSON"}), 400

    data = request.get_json()
    allowed_fields = {"title", "abstract", "img", "categories", "prod", "content"}
    fields = {k: v for k, v in data.items() if k in allowed_fields}

    if not fields:
        return jsonify({"message": "No se proporcionaron campos válidos para actualizar"}), 400

    try:
        updated = PostsService.update_post(post_id, fields)
        if not updated:
            return jsonify({"status": "error", "message": "Post no encontrado"}), 404
        return jsonify({"status": "success", "message": "Post actualizado correctamente", "id": post_id}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@posts_bp.route('/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Elimina un post por su ID.
    """
    try:
        deleted = PostsService.delete_post(post_id)
        if not deleted:
            return jsonify({"status": "error", "message": "Post no encontrado"}), 404
        return jsonify({"status": "success", "message": "Post eliminado correctamente", "id": post_id}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
