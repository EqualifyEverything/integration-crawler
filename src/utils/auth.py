import time
import pika
from utils.watch import logger


def rabbit(queue_name, message):
    while True:
        try:
            logger.debug('Connecting to RabbitMQ server...')
            credentials = pika.PlainCredentials('worker_crawler', 'explore_the_unknown')
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', credentials=credentials, virtual_host='gova11y'))
            logger.debug('Connected to RabbitMQ server!')

            logger.debug(f'Declaring queue: {queue_name}...')
            channel = connection.channel()
            channel.queue_declare(queue=queue_name, durable=True, arguments={'x-message-ttl': 7200000})
            logger.debug(f'Queue {queue_name} declared!')

            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message,
                properties=pika.BasicProperties(delivery_mode=2)  # Make the messages persistent
            )
            channel.close()
            connection.close()
            return channel, connection

        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Connection to RabbitMQ server failed: {e}")
            logger.info("Retrying connection in 10 seconds...")
            time.sleep(10)

        except Exception as e:
            logger.error(f"You've got a sick rabbit... {e}")
            return None, None


def catch_rabbits(queue_name, callback):
    while True:
        try:
            logger.debug('Connecting to RabbitMQ server...')
            credentials = pika.PlainCredentials(
                'worker_crawler', 'explore_the_unknown')
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                'rabbit', credentials=credentials, virtual_host='gova11y'))
            logger.debug('Connected to RabbitMQ server!')

            logger.debug(f'Declaring queue: {queue_name}...')
            channel = connection.channel()
            channel.queue_declare(
                queue=queue_name, durable=True,
                arguments={'x-message-ttl': 7200000})
            logger.debug(f'Queue {queue_name} declared!')

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue=queue_name,
                on_message_callback=callback,
                auto_ack=False)
            logger.info(f'🐇 [*] Waiting for messages in {queue_name}. ')
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Connection to RabbitMQ server failed: {e}")
            logger.info("Retrying connection in 10 seconds...")
            time.sleep(10)