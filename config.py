import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

    # PostgreSQL Configuration
    POSTGRES_URI_LOCAL = os.getenv("POSTGRES_URI_LOCAL")
    POSTGRES_URI_PROD = os.getenv("POSTGRES_URI_PROD")
    POSTGRES_URI = POSTGRES_URI_PROD if ENVIRONMENT == "production" else POSTGRES_URI_LOCAL

    # Mailchimp Configuration
    MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
    MAILCHIMP_DC = os.getenv('MAILCHIMP_DC')
    MAILCHIMP_LIST_ID = os.getenv('MAILCHIMP_LIST_ID')
