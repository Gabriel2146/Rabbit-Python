from kombu import Connection, Queue, Producer
import json


class RabbitMQService:
    """Service to manage RabbitMQ connection and queues."""

    def __init__(self, url, queue_name):
        self.url = url
        self.queue_name = queue_name

    def get_connection(self):
        """Establishes and returns a RabbitMQ connection."""
        try:
            return Connection(self.url)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to RabbitMQ: {e}")

    def get_queue(self):
        """Defines and returns the queue."""
        return Queue(self.queue_name, durable=True)


class EmailSender:
    """Service to send email messages via RabbitMQ."""

    def __init__(self, rabbit_service):
        self.rabbit_service = rabbit_service

    def validate_email_data(self, email_data):
        """
        Validates the email data structure.
        :param email_data: Dictionary with 'to', 'subject', and 'body'.
        :raises ValueError: If required keys are missing or values are invalid.
        """
        required_keys = ["to", "subject", "body"]
        for key in required_keys:
            if key not in email_data or not isinstance(email_data[key], str):
                raise ValueError(f"Invalid or missing '{key}' in email data.")

    def send_email(self, email_data):
        """
        Publishes an email message to the RabbitMQ queue.
        :param email_data: Dictionary with 'to', 'subject', and 'body'.
        """
        self.validate_email_data(email_data)  # Validar datos antes de enviarlos

        try:
            with self.rabbit_service.get_connection() as conn:
                channel = conn.channel()
                queue = self.rabbit_service.get_queue()
                producer = Producer(channel)
                producer.publish(
                    json.dumps(email_data),  # Serializa a JSON
                    exchange=queue.exchange,
                    routing_key=queue.name,
                    declare=[queue],
                    serializer="json",
                )
                print(f"Message sent successfully to {email_data['to']}.")
        except Exception as e:
            raise RuntimeError(f"Failed to send message: {e}")


if __name__ == "__main__":
    # URL de conexión usando el contenedor 'rabbit' y credenciales de Docker Compose
    RABBIT_URL = "amqp://GabrielP:2146@localhost:5672/"  # Cambiar 'localhost' a 'rabbit' si ejecutas desde un contenedor
    QUEUE_NAME = "email_queue"

    # Crear instancia de RabbitMQService y EmailSender
    rabbit_service = RabbitMQService(RABBIT_URL, QUEUE_NAME)
    email_sender = EmailSender(rabbit_service)

    # Email a enviar
    email_message = {
        "to": "example@example.com",
        "subject": "Test Email",
        "body": "Hello, this is a test email message sent via RabbitMQ and Kombu!",
    }

    # Enviar el correo
    try:
        email_sender.send_email(email_message)
    except (ValueError, ConnectionError, RuntimeError) as error:
        print(f"Error: {error}")

