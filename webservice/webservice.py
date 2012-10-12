'''
Copyright (c) 2012, Donald Talton
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer. Redistributions in
binary form must reproduce the above copyright notice, this list of
conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

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
