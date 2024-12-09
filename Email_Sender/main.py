from rabbitmq_service import RabbitMQService
from email_sender import EmailSender

if __name__ == "__main__":
    # RabbitMQ URL and queue configuration
    RABBIT_URL = "amqp://GabrielP:2146@localhost:5672/"  # Replace 'localhost' with 'rabbit' for Docker
    QUEUE_NAME = "email_queue"

    # Create service instances
    rabbit_service = RabbitMQService(RABBIT_URL, QUEUE_NAME)
    email_sender = EmailSender(rabbit_service)

    # Define the email to send
    email_message = {
        "to": "example@example.com",
        "subject": "Test Email",
        "body": "Hello, this is a test email message sent via RabbitMQ and Kombu!",
    }

    # Send the email
    try:
        email_sender.send_email(email_message)
    except (ValueError, ConnectionError, RuntimeError) as error:
        print(f"Error: {error}")
