from email_receiver.rabbitmq_service import RabbitMQService
from email_receiver.email_receiver import EmailReceiver
from email_receiver.email_handler import email_handler
from config import RABBITMQ

if __name__ == "__main__":
    # Usa la configuración para inicializar el servicio
    rabbit_service = RabbitMQService(RABBITMQ["URL"], RABBITMQ["QUEUE_NAME"])
    email_receiver = EmailReceiver(rabbit_service, email_handler)

    try:
        email_receiver.start_receiving()
    except Exception as e:
        print(f"Critical error: {e}")
