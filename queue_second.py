from second_recall import second_recall
import pika

second_recall = second_recall()
print(second_recall)
# def main():
#     credentials = pika.PlainCredentials('user', 'Qq1234567!')
#     parameters = pika.ConnectionParameters('localhost', 5673, '/', credentials)
#     connection = pika.BlockingConnection(parameters)
#     channel = connection.channel()
#
#     channel.queue_declare(queue='queue_second')
#
#     channel.basic_publish(exchange='', routing_key='queue_second', body=f'{second_recall}')
#
#     connection.close()
#
#
# main()
