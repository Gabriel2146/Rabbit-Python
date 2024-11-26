from kombu import Connection, Queue, Consumer
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


class EmailReceiver:
    """Service to receive and process email messages from RabbitMQ."""

    def __init__(self, rabbit_service, message_handler):
        self.rabbit_service = rabbit_service
        self.message_handler = message_handler

    def start_receiving(self):
        """Starts listening to the RabbitMQ queue."""
        with self.rabbit_service.get_connection() as conn:
            channel = conn.channel()
            queue = self.rabbit_service.get_queue()
            consumer = Consumer(
                channel, queue, callbacks=[self.message_handler], accept=["json"]
            )
            with consumer:
                print("Waiting for messages. Press CTRL+C to exit.")
                try:
                    while True:
                        conn.drain_events(timeout=1)
                except KeyboardInterrupt:
                    print("Stopped receiving messages.")


def email_handler(body, message):
    """
    Handles the received email message.
    :param body: The message body received from the queue.
    :param message: The message object.
    """
    email = json.loads(body)
    print("Received a message:")
    print(f"To: {email['to']}")
    print(f"Subject: {email['subject']}")
    print(f"Body: {email['body']}")
    message.ack()


if __name__ == "__main__":
    # URL de conexión usando el contenedor 'rabbit' y credenciales de Docker Compose
    RABBIT_URL = "amqp://GabrielP:2146@rabbit:5672/"
    QUEUE_NAME = "email_queue"

    # Crear instancia de RabbitMQService y EmailReceiver
    rabbit_service = RabbitMQService(RABBIT_URL, QUEUE_NAME)
    email_receiver = EmailReceiver(rabbit_service, email_handler)

    # Iniciar recepción de correos
    email_receiver.start_receiving() 
