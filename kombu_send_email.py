from kombu import Connection, Queue, Producer
import json


class RabbitMQService:
    """Service to manage RabbitMQ connection and queues."""

    def __init__(self, url, queue_name):
        self.url = url
        self.queue_name = queue_name

    def get_connection(self):
        """Establishes and returns a RabbitMQ connection."""
        return Connection(self.url)

    def get_queue(self):
        """Defines and returns the queue."""
        return Queue(self.queue_name, durable=True)


class EmailSender:
    """Service to send email messages via RabbitMQ."""

    def __init__(self, rabbit_service):
        self.rabbit_service = rabbit_service

    def send_email(self, email_data):
        """
        Publishes an email message to the RabbitMQ queue.
        :param email_data: Dictionary with 'to', 'subject', and 'body'.
        """
        with self.rabbit_service.get_connection() as conn:
            channel = conn.channel()
            queue = self.rabbit_service.get_queue()
            producer = Producer(channel)
            producer.publish(
                json.dumps(email_data),
                exchange=queue.exchange,
                routing_key=queue.name,
                declare=[queue],
                serializer="json",
            )
            print("Message sent successfully!")


if __name__ == "__main__":
    # URL de conexión usando el contenedor 'rabbit' y credenciales de Docker Compose
    RABBIT_URL = "amqp://GabrielP:2146@rabbit:5672/"
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
    email_sender.send_email(email_message)
