import logging
log = logging.getLogger("zen.useraction.actions")
from socket import getaddrinfo

import Globals

from zope.interface import implements

import pika

from Products.ZenUtils.guid.guid import GUIDManager
from Products.ZenModel.interfaces import IAction
from Products.ZenModel.actions import  _signalToContextDict, ActionExecutionException, IActionBase


from ZenPacks.SteelHouseLabs.EventForwarder.interfaces import IEventForwarderActionContentInfo

from Products.ZenUtils.GlobalConfig import getGlobalConfiguration

class EventForwarderAction(IActionBase):
    implements(IAction)

    id = 'eventForwarder'
    name = 'Event Forwarder'
    actionContentInfo = IEventForwarderActionContentInfo
    global_conf = getGlobalConfiguration()

    exchange = 'events'
    queue = 'eventForwarder'
    passwd = global_conf.get('amqppassword', 'zenoss')
    user = global_conf.get('amqpuser', 'zenoss')
    vhost = global_conf.get('amqpvhost', '/zenoss')
    port = int(global_conf.get('amqpport', '5672'))
    host = global_conf.get('amqphost', 'localhost')

    credentials = pika.PlainCredentials(user, passwd)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host = host, port = port, virtual_host = vhost, credentials = credentials))

    channel = connection.channel()

    channel.exchange_declare(exchange = exchange,
                                type = "fanout",
                                auto_delete = False,
                                durable = True)

    channel.queue_declare(queue = queue,
                             auto_delete = False,
                             exclusive = False,
                             durable = True)


    def setupAction(self, dmd):
        self.guidManager = GUIDManager(dmd)

    def execute(self, notification, signal):
        """
        Forward events to the eventForwarder rabbit queue. 
        """
        log.debug('Processing Forwarder action.')
        self.setupAction(notification.dmd)
        data = _signalToContextDict(signal, self.options.get('zopeurl'), notification, self.guidManager)

        if signal.clear and data['clearEventSummary'].uuid:
            self._sendToQueue(notification, data, data['clearEventSummary'], self.channel, self.exchange)

        self._sendToQueue(notification, data, data['eventSummary'], self.channel, self.exchange)

    def _sendToQueue(self, notification, data, event, channel, exchange):
        actor = getattr(event, "actor", None)
        details = event.details

        fields = {
           'uuid' :                         ( 1, event),
           'fingerprint' :                  ( 2, event),
           'element_identifier' :           ( 3, actor),
           'element_sub_identifier' :       ( 4, actor),
           'event_class' :                  ( 5, event),
           'event_key' :                    ( 6, event),
           'event_key' :                    ( 6, event),
           'summary' :                      ( 7, event),
           'message' :                      ( 8, event),
           'severity' :                     ( 9, event),
           'status' :                       (10, event),
           'event_class_key' :              (11, event),
           'event_group' :                  (12, event),
           'state_change_time' :            (13, event),
           'first_seen_time' :              (14, event),
           'last_seen_time' :               (15, event),
           'count' :                        (16, event),
           'zenoss.device.production_state':(17, details),
           'agent':                         (20, event),
           'zenoss.device.device_class':    (21, details),
           'zenoss.device.location' :       (22, details),
           'zenoss.device.systems' :        (23, details),
           'zenoss.device.groups' :         (24, details),
           'zenoss.device.ip_address':      (25, details),
           'syslog_facility' :              (26, event),
           'syslog_priority' :              (27, event),
           'nt_event_code' :                (28, event),
           'current_user_name' :            (29, event),
           'cleared_by_event_uuid' :        (31, event),
           'zenoss.device.priority' :       (32, details),
           'event_class_mapping_uuid':      (33, event),
           'element_title':                 (34, actor),
           'element_sub_title':             (35, actor)
           }

        eventDict = self.createEventDict(fields, event)
        self.processEventDict(eventDict, data, notification.dmd)


        eventDict = self.createEventDict(fields, event)
        self.processEventDict(eventDict, data, notification.dmd)

        self.channel.basic_publish(exchange=self.exchange,
                      routing_key='eventForwarder',
                      body=str(eventDict))



    def createEventDict(self, fields, event):
        """
        Create an event dictionary suitable for Python evaluation.
        """
        eventDict = {}
        for field, oidspec in fields.items():
            i, source = oidspec
            if source is event.details:
                val = source.get(field, '')
            else:
                val = getattr(source, field, '')
            eventDict[field] = val
        return eventDict

    def processEventDict(self, eventDict, data, dmd):
        """
        Integration hook
        """
        pass


    def updateContent(self, content=None, data=None):
        pass
