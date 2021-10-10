from last_recall import last_recall
import pika

last_recall = last_recall()
# print(last_recall)


def main():
    credentials = pika.PlainCredentials('user', 'Qq1234567!')
    parameters = pika.ConnectionParameters('192.168.40.10', 5673, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='queue_last')

    channel.basic_publish(exchange='', routing_key='queue_last', body=f'{last_recall}')

    connection.close()


main()
