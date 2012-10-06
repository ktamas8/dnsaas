import web
import pika
import json
import sys

'''
put this pika shit into a conf at some point
'''
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='dns', durable=True)
except:
    sys.exit("Exiting: unable to connect to rabbitmq-server")

        
urls = (
    '/add', 'add',
    '/delete', 'delete',
    '/update', 'update'
)
app = web.application(urls, globals())

class hello:        
    def GET(self, name):
        if not name: 
            name = 'World'
        return 'Hello, ' + name + '!'

class add:
    def POST(self):
        user_data = web.input()
        host = user_data.hostname.partition(".")[0]
        ip = user_data.ip
        record_type = user_data.type
        action = "add"
        request = json.dumps([action, host, ip, record_type])
        try:
            channel.basic_publish(exchange='', routing_key='dns', 
                                  body=request, properties=pika.BasicProperties(
                                      delivery_mode = 2,
                                  ))
            return request
        except:
            print "unable to publish message"
            return

class delete:
    def POST(self, name):
        if not name:
            name = 'World'
        return 'Hello, ' + name + '!'

class update:
    def POST(self, name):
        if not name:
            name = 'World'
        return 'Hello, ' + name + '!'

if __name__ == "__main__":
    app.run()
