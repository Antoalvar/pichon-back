import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from pymongo import MongoClient
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import requests

app = Flask(__name__)

load_dotenv()

#Credentials

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["pichon"]
post_collection = db["posts"]

mailchimp_api_key = os.getenv('MAILCHIMP_API_KEY')
mailchimp_dc = os.getenv('MAILCHIMP_DC')
mailchimp_list_id = os.getenv('MAILCHIMP_LIST_ID')

mailchimp = Client()
mailchimp.set_config({
  "api_key": mailchimp_api_key,
  "server": mailchimp_dc
})

response = mailchimp.ping.get()
print(response)


def subscribe_user_to_mailchimp(email_address, first_name, last_name=""):
    payload = {
        "email_address": email_address,
        "status": "subscribed",
        "merge_fields": {
            "FNAME": first_name,
            "LNAME": last_name
        }
    }

    try:
        response = mailchimp.lists.add_list_member(mailchimp_list_id, payload)
        return True, "response: {}".format(response)

    except ApiClientError as error:
        return False, "An exception occurred: {}".format(error.text)

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return False, "No se pudo conectar con el servidor de Mailchimp."

#Routes

@app.route("/posts", methods=["GET"])
def get_posts():
    posts = list(post_collection.find({}, {"_id": 0}))
    return jsonify(posts)

@app.route("/posts/<post_id>", methods=["GET"])
def get_post_by_id(post_id):
    post = post_collection.find_one({"post_id": post_id}, {"_id": 0})
    if post:
        return jsonify(post)
    else:
        return jsonify({"message": "Post not founf"}), 404

@app.route("/posts", methods=["POST"])
def add_post():
    post = request.json
    if not post.get("post_id") or post_collection.find_one({"post_id": post["post_id"]}):
        return jsonify({"message": "Id required and must be unique"})

    post_collection.insert_one(post)
    return jsonify({"message": "Post created"}), 201

@app.route("/posts/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    print("HOLA")
    result = post_collection.delete_one({"post_id": post_id})

    if result.deleted_count:
        return jsonify({"message": "Post Deleted"}), 200

    else:
        return jsonify({"message": "Post not found"}), 404

@app.route("/subscribe_newsletter", methods=["POST"])
def subscribe_newsletter():
    """
    Endpoint de la API que recibe datos JSON de Angular
    y suscribe al usuario a Mailchimp.
    """

    # 1. Verificar que la petición contenga datos JSON
    if not request.is_json:
        return jsonify({"message": "Falta el body en formato JSON"}), 400

    # 2. Extraer los datos del cuerpo JSON de la petición
    data = request.get_json()
    email = data.get('email', None)
    fname = data.get('fname', None) # Asumimos que Angular envía 'fname'

    # Validaciones básicas
    if not email:
        return jsonify({"message": "El campo 'email' es obligatorio"}), 400

    # 3. Llamar a la función que interactúa con la API de Mailchimp
    success, message = subscribe_user_to_mailchimp(email, fname)

    # 4. Devolver la respuesta adecuada a Angular
    if success:
        # Respuesta estándar 200 OK para éxito
        return jsonify({"status": "success", "message": message}), 200
    else:
        # Respuesta estándar 400 Bad Request o 409 Conflict para errores de negocio
        status_code = 409 if "suscrito" in message else 400
        return jsonify({"status": "error", "message": message}), status_code


if __name__ == "__main__":
    app.run(debug=True)