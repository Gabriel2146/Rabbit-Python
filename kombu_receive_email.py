# kombu_receive_email.py
from kombu import Connection, Queue, Consumer
import json

# URL de conexión a RabbitMQ configurado en el docker-compose
rabbit_url = "amqp://GabrielP:2146@localhost:5672/"

# Crear una conexión con RabbitMQ
with Connection(rabbit_url) as conn:
    # Crear un canal de comunicación
    channel = conn.channel()

    # Definir la cola
    email_queue = Queue('email_queue', durable=True)

    # Callback que se ejecuta cuando un mensaje es recibido
    def callback(body, message):
        # Convertir el mensaje de JSON a diccionario
        email = json.loads(body)
        
        # Imprimir el correo recibido
        print(f"Received a message:")
        print(f"To: {email['to']}")
        print(f"Subject: {email['subject']}")
        print(f"Body: {email['body']}")
        
        # Acknowledgement (confirmación de recepción)
        message.ack()

    # Crear un consumidor
    consumer = Consumer(channel, email_queue, callbacks=[callback], accept=['json'])

    # Iniciar el consumidor
    with consumer:
        print("Waiting for messages. Press CTRL+C to exit.")
        
        # Consume mensajes de la cola
        consumer.consume()

        # Bloquear para escuchar los mensajes
        conn.drain_events()
