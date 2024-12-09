import json

def email_handler(body, message):
    """
    Handles the received email message.
    :param body: The message body received from the queue.
    :param message: The message object.
    """
    try:
        email = json.loads(body)
        if not all(key in email for key in ["to", "subject", "body"]):
            raise ValueError("Message is missing required fields: 'to', 'subject', 'body'.")

        print("Received a message:")
        print(f"To: {email['to']}")
        print(f"Subject: {email['subject']}")
        print(f"Body: {email['body']}")
        message.ack()  # Acknowledge the message
    except json.JSONDecodeError:
        print("Failed to decode message. Rejecting...")
        message.reject()
    except ValueError as ve:
        print(f"Invalid message structure: {ve}")
        message.reject()
    except Exception as e:
        print(f"Unexpected error: {e}")
        message.reject()
