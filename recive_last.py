import pika
from datetime import datetime
from asterisk.ami import AMIClient
from asterisk.ami import AMIClientAdapter


def callback(ch, method, properties, body):
    if body:
        client = AMIClient(address='192.168.40.10', port=5038)
        client.login(username='admin', secret='111')
        body = str(body)
        body = body.replace('b', '')
        body = body.replace('\'', '')
        with open('log_last_recall.txt', mode='a', encoding='utf-8') as f:
            f.write(f"'called' {body} - {datetime.now()}\n")
        adapter = AMIClientAdapter(client)
        adapter.Originate(
            Channel='Local/15020@third_recall',
            Exten=body,
            Priority=1,
            Context='third_recall',
            Timeout=600000,
            CallerID=body, )
        client.logoff()


def main():
    credentials = pika.PlainCredentials('user', 'Qq1234567!')
    parameters = pika.ConnectionParameters('192.168.40.10', 5673, '/', credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    method, props, body = channel.basic_get('queue_last', auto_ack=True)
    if body:
        callback('queue_last', method, props, body)
    connection.close()


main()
