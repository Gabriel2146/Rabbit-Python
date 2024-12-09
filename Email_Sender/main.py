from email_sender.rabbitmq_service import RabbitMQService
from email_sender.email_sender import EmailSender
from config import RABBITMQ

if __name__ == "__main__":
    # Usa la configuración para inicializar el servicio
    rabbit_service = RabbitMQService(RABBITMQ["URL"], RABBITMQ["QUEUE_NAME"])
    email_sender = EmailSender(rabbit_service)

    email_message = {
        "to": "example@example.com",
        "subject": "Test Email",
        "body": "Hello, this is a test email message sent via RabbitMQ and Kombu!",
    }

    try:
        email_sender.send_email(email_message)
    except (ValueError, ConnectionError, RuntimeError) as error:
        print(f"Error: {error}")
