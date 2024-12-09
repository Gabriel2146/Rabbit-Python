from kombu import Consumer

class EmailReceiver:
    """Service to receive and process email messages from RabbitMQ."""

    def __init__(self, rabbit_service, message_handler):
        self.rabbit_service = rabbit_service
        self.message_handler = message_handler

    def start_receiving(self):
        """Starts listening to the RabbitMQ queue."""
        try:
            with self.rabbit_service.get_connection() as conn:
                channel = conn.channel()
                queue = self.rabbit_service.get_queue()
                consumer = Consumer(
                    channel, queues=[queue], callbacks=[self.message_handler], accept=["json"]
                )
                with consumer:
                    print("Waiting for messages. Press CTRL+C to exit.")
                    while True:
                        try:
                            conn.drain_events(timeout=1)
                        except TimeoutError:
                            pass  # No message yet, continue waiting
        except KeyboardInterrupt:
            print("Stopped receiving messages.")
        except Exception as e:
            print(f"Error occurred while receiving messages: {e}")
