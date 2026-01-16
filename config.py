import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # PostgreSQL Configuration
    POSTGRES_URI_LOCAL = os.getenv(
        "POSTGRES_URI_LOCAL",
        "postgresql://manager:ThaoGZ5n9XowXVpWFEHzKWLqaYlmU8uL@dpg-d5l7ili4d50c73e16830-a.virginia-postgres.render.com/pichon_db"
    )
    POSTGRES_URI_PROD = os.getenv(
        "POSTGRES_URI_PROD",
        "postgresql://manager:ThaoGZ5n9XowXVpWFEHzKWLqaYlmU8uL@dpg-d5l7ili4d50c73e16830-a/pichon_db"
    )
    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
    POSTGRES_URI = POSTGRES_URI_PROD if ENVIRONMENT == "production" else POSTGRES_URI_LOCAL

    # Mailchimp Configuration
    MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
    MAILCHIMP_DC = os.getenv('MAILCHIMP_DC')
    MAILCHIMP_LIST_ID = os.getenv('MAILCHIMP_LIST_ID')
