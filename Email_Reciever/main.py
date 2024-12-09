from dotenv import load_dotenv
import os
from rabbitmq_service import RabbitMQService
from email_receiver import EmailReceiver
from handlers import email_handler

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

if __name__ == "__main__":
    # Obtener la URL de conexión y el nombre de la cola desde las variables de entorno
    RABBIT_URL = os.getenv("RABBIT_URL")  # Leer desde .env
    QUEUE_NAME = os.getenv("QUEUE_NAME")  # Leer desde .env

    # Crear servicio de RabbitMQ
    rabbit_service = RabbitMQService(RABBIT_URL, QUEUE_NAME)

    # Crear la instancia del receptor de correos
    email_receiver = EmailReceiver(rabbit_service, email_handler)

    # Intentar recibir los correos
    try:
        email_receiver.start_receiving()
    except Exception as e:
        print(f"Error al recibir mensajes: {e}")
