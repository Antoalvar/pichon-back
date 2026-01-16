from flask import Blueprint, request, jsonify
from app.services.mailchimp_service import MailchimpService

newsletter_bp = Blueprint('newsletter', __name__, url_prefix='')

mailchimp_service = MailchimpService()


@newsletter_bp.route("/subscribe_newsletter", methods=["POST"])
def subscribe_newsletter():
    """
    Endpoint para suscribir un usuario a la newsletter de Mailchimp.
    Recibe: email (requerido), fname (nombre), lname (apellido, opcional)
    """

    # 1. Verificar que la petición contenga datos JSON
    if not request.is_json:
        return jsonify({"message": "Falta el body en formato JSON"}), 400

    # 2. Extraer los datos del cuerpo JSON de la petición
    data = request.get_json()
    email = data.get('email', None)
    fname = data.get('fname', None)
    lname = data.get('lname', "")

    # 3. Validaciones básicas
    if not email:
        return jsonify({"message": "El campo 'email' es obligatorio"}), 400

    # 4. Llamar al servicio de Mailchimp
    success, message = mailchimp_service.subscribe_user(email, fname, lname)

    # 5. Devolver la respuesta adecuada
    if success:
        return jsonify({"status": "success", "message": message}), 200
    else:
        status_code = 409 if "suscrito" in message else 400
        return jsonify({"status": "error", "message": message}), status_code
