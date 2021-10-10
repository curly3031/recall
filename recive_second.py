import pika
from datetime import datetime
from asterisk.ami import AMIClient
from asterisk.ami import AMIClientAdapter


def callback(ch, method, properties, body):
    if body:
        client = AMIClient(address='127.0.0.1', port=5038)
        client.login(username='admin', secret='111')
        body = str(body)
        body = body.replace('b', '')
        body = body.replace('\'', '')
        with open('log_first_recall.txt', mode='a', encoding='utf-8') as f:
            f.write(f"'called' {body} - {datetime.now()}\n")
        adapter = AMIClientAdapter(client)
        adapter.Originate(
            Channel='Local/15010@second_recall',
            Exten=body,
            Priority=1,
            Context='second_recall',
            Timeout=600000,
            CallerID=body,)
        client.logoff()


def main():
    credentials = pika.PlainCredentials('user', 'Qq1234567!')
    parameters = pika.ConnectionParameters('localhost', 5673, '/', credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    method, props, body = channel.basic_get('queue_second', auto_ack=True)
    if body:
        callback('queue_second', method, props, body)
    connection.close()


main()
