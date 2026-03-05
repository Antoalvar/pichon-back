from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import requests
import hashlib
from config import Config


class MailchimpService:
    def __init__(self):
        self.mailchimp = Client()
        self.mailchimp.set_config({
            "api_key": Config.MAILCHIMP_API_KEY,
            "server": Config.MAILCHIMP_DC
        })

    def trigger_info_email(self, email_address, first_name, journey_id, step_id):
        """
        Triggers a Mailchimp Customer Journey step to send an info email immediately.

        Args:
            email_address (str): Recipient email
            first_name (str): Recipient name
            journey_id (int): Mailchimp Customer Journey ID
            step_id (int): Mailchimp Journey step ID to trigger

        Returns:
            tuple: (success: bool, message: str)
        """
        payload = {
            "email_address": email_address,
            "merge_fields": {
                "FNAME": first_name
            }
        }

        try:
            self.mailchimp.customerJourneys.trigger(journey_id, step_id, payload)
            return True, "Info email triggered successfully."

        except ApiClientError as error:
            return False, f"An exception occurred: {error.text}"

        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return False, "No se pudo conectar con el servidor de Mailchimp."

    def subscribe_user(self, email_address, first_name, last_name=""):
        """
        Suscribe (o reactiva) un usuario en la lista de Mailchimp.
        Usa el endpoint PUT (upsert) para manejar contactos nuevos, existentes
        y aquellos que fueron eliminados permanentemente.

        Args:
            email_address (str): Email del usuario
            first_name (str): Nombre del usuario
            last_name (str): Apellido del usuario (opcional)

        Returns:
            tuple: (success: bool, message: str)
        """
        subscriber_hash = hashlib.md5(email_address.lower().encode()).hexdigest()

        payload = {
            "email_address": email_address,
            "status_if_new": "subscribed",
            "status": "subscribed",
            "merge_fields": {
                "FNAME": first_name,
                "LNAME": last_name
            }
        }

        try:
            response = self.mailchimp.lists.set_list_member(
                Config.MAILCHIMP_LIST_ID, subscriber_hash, payload
            )
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
