import os

try:
    from dotenv import load_dotenv

    # Cargar variables del archivo .env (si existe)
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using default environment variables.")

RABBITMQ = {
    "URL": os.getenv("RABBITMQ_URL", "amqp://GabrielP:2146@localhost:5672/"),
    "QUEUE_NAME": os.getenv("RABBITMQ_QUEUE_NAME", "email_queue"),
}
