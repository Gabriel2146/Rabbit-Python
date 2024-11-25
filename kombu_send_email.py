# kombu_send_email.py
from kombu import Connection, Queue, Producer
import json

# URL de conexión a RabbitMQ configurado en el docker-compose
rabbit_url = "amqp://GabrielP:2146@localhost:5672/"

# Crear una conexión con RabbitMQ
with Connection(rabbit_url) as conn:
    # Crear un canal de comunicación
    channel = conn.channel()

    # Definir la cola
    email_queue = Queue('email_queue', durable=True)

    # Crear el mensaje (representando un correo electrónico)
    message = {
        'to': 'example@example.com',
        'subject': 'Test Email',
        'body': 'Hello, this is a test email message sent via RabbitMQ and Kombu!'
    }

    # Publicar el mensaje en la cola
    producer = Producer(channel)
    producer.publish(
        json.dumps(message),  # Convertir el mensaje a JSON
        exchange=email_queue.exchange,
        routing_key=email_queue.name,
        declare=[email_queue],
        serializer='json'  # El mensaje se enviará en formato JSON
    )

    print("Message sent successfully!")
