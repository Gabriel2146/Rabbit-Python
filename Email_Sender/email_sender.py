import json
from kombu import Producer

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
        self.validate_email_data(email_data)  # Validate data before sending

        try:
            with self.rabbit_service.get_connection() as conn:
                channel = conn.channel()
                queue = self.rabbit_service.get_queue()
                producer = Producer(channel)
                producer.publish(
                    json.dumps(email_data),  # Serialize to JSON
                    exchange=queue.exchange,
                    routing_key=queue.name,
                    declare=[queue],
                    serializer="json",
                )
                print(f"Message sent successfully to {email_data['to']}.")
        except Exception as e:
            raise RuntimeError(f"Failed to send message: {e}")
