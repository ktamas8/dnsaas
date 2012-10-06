import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='dns', durable=True)


def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    try:
        print "connect to dns, do shit successfully"
        ch.basic_ack(delivery_tag = method.delivery_tag)
    except:
        print "i failed, no msg ack"

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,queue='dns')

print ' waiting for messages '
channel.start_consuming()







connection.close
