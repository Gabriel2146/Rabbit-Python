from rabbitmq_service import RabbitMQService
from email_receiver import EmailReceiver
from handlers import email_handler

if __name__ == "__main__":
    # Connection URL using RabbitMQ and Docker credentials
    RABBIT_URL = "amqp://GabrielP:2146@localhost:5672/"  # Replace 'localhost' with 'rabbit' for Docker
    QUEUE_NAME = "email_queue"

    # Create instances
    rabbit_service = RabbitMQService(RABBIT_URL, QUEUE_NAME)
    email_receiver = EmailReceiver(rabbit_service, email_handler)

    # Start consuming emails
    try:
        email_receiver.start_receiving()
    except Exception as e:
        print(f"Critical error: {e}")
