from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import requests
from config import Config


class MailchimpService:
    def __init__(self):
        self.mailchimp = Client()
        self.mailchimp.set_config({
            "api_key": Config.MAILCHIMP_API_KEY,
            "server": Config.MAILCHIMP_DC
        })

    def subscribe_user(self, email_address, first_name, last_name=""):
        """
        Suscribe un usuario a la lista de Mailchimp.
        
        Args:
            email_address (str): Email del usuario
            first_name (str): Nombre del usuario
            last_name (str): Apellido del usuario (opcional)
        
        Returns:
            tuple: (success: bool, message: str)
        """
        payload = {
            "email_address": email_address,
            "status": "subscribed",
            "merge_fields": {
                "FNAME": first_name,
                "LNAME": last_name
            }
        }

        try:
            response = self.mailchimp.lists.add_list_member(Config.MAILCHIMP_LIST_ID, payload)
            return True, f"response: {response}"

        except ApiClientError as error:
            return False, f"An exception occurred: {error.text}"

        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return False, "No se pudo conectar con el servidor de Mailchimp."

    @staticmethod
    def ping():
        """Verifica la conexión con Mailchimp."""
        mailchimp = Client()
        mailchimp.set_config({
            "api_key": Config.MAILCHIMP_API_KEY,
            "server": Config.MAILCHIMP_DC
        })
        return mailchimp.ping.get()
