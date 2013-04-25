#!/usr/bin/env python
import pika

import Globals
from Products.ZenUtils.GlobalConfig import getGlobalConfiguration

global_conf = getGlobalConfiguration()

exchange = 'events'
queue = 'eventForwarder'
passwd = global_conf.get('amqppassword', 'zenoss')
user = global_conf.get('amqpuser', 'zenoss')
vhost = global_conf.get('amqpvhost', '/zenoss')
port = int(global_conf.get('amqpport', '5672'))
host = global_conf.get('amqphost', 'localhost')

credentials = pika.PlainCredentials(user, passwd)

connection = pika.BlockingConnection(pika.ConnectionParameters(host = host,
                                         port = port,
                                         virtual_host = vhost,
                                         credentials = credentials))

channel = connection.channel()

channel.queue_bind(exchange='events',
                   queue=queue)

print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] %r" % (body,)

channel.basic_consume(callback,
                      queue=queue,
                      no_ack=True)

channel.start_consuming()
