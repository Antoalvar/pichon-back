from flask import Blueprint, request, jsonify
from app.services.categories_service import CategoriesService

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@categories_bp.route('', methods=['GET'])
def get_categories():
    """
    Obtiene todas las categorías de la base de datos.
    """
    try:
        categories = CategoriesService.get_all_categories()
        return jsonify({
            "status": "success",
            "data": categories,
            "count": len(categories)
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@categories_bp.route('', methods=['POST'])
def create_category():
    """
    Crea una nueva categoría en la base de datos.
    Recibe: title (string), order (int)
    El slug se genera automáticamente a partir del título.
    """
    if not request.is_json:
        return jsonify({"message": "Falta el body en formato JSON"}), 400

    data = request.get_json()
    if 'title' not in data or 'order' not in data:
        return jsonify({"message": "Los campos 'title' y 'order' son obligatorios"}), 400

    title = data['title']
    order = data['order']
    slug = title.lower().replace(' ', '_')

    try:
        category_id = CategoriesService.create_category(name=title, slug=slug, order=order)
        return jsonify({
            "status": "success",
            "message": "Categoría creada correctamente",
            "id": category_id,
            "slug": slug
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
