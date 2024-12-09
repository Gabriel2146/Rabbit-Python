from kombu import Connection, Queue

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
