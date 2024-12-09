from dotenv import load_dotenv
import os
from rabbitmq_service import RabbitMQService
from email_sender import EmailSender

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

if __name__ == "__main__":
    # Obtener la URL de conexión y el nombre de la cola desde las variables de entorno
    RABBIT_URL = os.getenv("RABBIT_URL")  # Leer desde .env
    QUEUE_NAME = os.getenv("QUEUE_NAME")  # Leer desde .env

    # Crear servicio de RabbitMQ y emisor de email
    rabbit_service = RabbitMQService(RABBIT_URL, QUEUE_NAME)
    email_sender = EmailSender(rabbit_service)

    # Definir el email a enviar
    email_message = {
        "to": "example@example.com",
        "subject": "Test Email",
        "body": "Hello, this is a test email message sent via RabbitMQ and Kombu!",
    }

    # Enviar el email
    try:
        email_sender.send_email(email_message)
    except (ValueError, ConnectionError, RuntimeError) as error:
        print(f"Error: {error}")
