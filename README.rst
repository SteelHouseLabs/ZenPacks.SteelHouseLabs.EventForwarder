===============================================================================
ZenPacks.SteelHouseLabs.EventForwarder
===============================================================================


About
-------------------------------------------------------------------------------
This ZenPack adds new event notification actions that are used by the
``zenactiond`` daemon.


Features
-------------------------------------------------------------------------------

The Event Forwarder action forwards events to the eventForwarder rabbit queue. Destination extension packs, such as ZenPacks.SteelHouseLabs.SplunkForwarder and ZenPacks.SteelHouseLabs.ZenossForwarder, can then consume this queue and process events to their appropriate destination.


Prerequisites
-------------------------------------------------------------------------------

==================  =========================================================
Prerequisite        Restriction
==================  =========================================================
Product             Zenoss 4.1.1 or higher
Required ZenPacks   None
Other dependencies  pika 0.98
==================  =========================================================


Limitations
-------------------------------------------------------------------------------
These notification actions are not able to provide immediate feedback as to
whether or not configuration information is correct, so the ``zenactiond.log``
file must be checked to ensure that the actions are working correctly.


Usage
-------------------------------------------------------------------------------
See the Zenoss Service Dynamics Administration Guide for more information about
triggers and notifications. Any issues detected during the run of the
notification will result in an event sent to the event console as well as a
message in the ``zenactiond.log`` file.


Select the Event Forwarder Action
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This assumes that the appropriate triggers have already been set up.

1. Navigate to ``Events`` -> ``Triggers`` page.

2. Click on the ``Notifications`` menu item.

3. Click on the plus sign ('+') to add a new notification.

4. From the dialog box, specify the name of the notification and select the
   ``Event Forwarder`` action.

5. Enable the notification and add a trigger to be associated with this action.

6. Click on the ``Submit`` button.


Installing
-------------------------------------------------------------------------------

Install the ZenPack via the command line and restart Zenoss::

    zenpack --install ZenPacks.SteelHouseLabs.EventForwarder-<version>.egg
    zenoss restart


Removing
-------------------------------------------------------------------------------

To remove the ZenPack, use the following command::

    zenpack --remove ZenPacks.SteelHouseLabs.EventForwarder
    zenoss restart


Troubleshooting
-------------------------------------------------------------------------------

The Zenoss support team will need the following output:

1. Set the ``zenhub`` daemon into ``DEBUG`` level logging by typing
   ``zenhub debug`` from the command-line. This will ensure that we can see the
   incoming event in the ``zenhub.log`` file.

2. Set the ``zenactiond`` daemon into ``DEBUG`` level logging by typing
   ``zenactiond debug`` from the command-line. This will ensure that we can see
   the incoming notification request and processing activity in the
   ``zenactiond.log`` file.

3. Create an event from the remote source, by the ``zensendevent`` command or by
   the event console ``Add an Event`` button. This event must match the trigger
   definition that will invoke your notification action.

4. Verify that the event was processed by the ``zenhub`` daemon by examining the
   ``zenhub.log`` file.

5. Wait for the ``zenactiond`` daemon to receive and then process the
   notification request.

6. In the case of errors an event will be generated and sent to the event
   console.

7. Running rabbitmqctl -p /zenoss list_queues should show a 'eventForwarder' queue once after the Notification is enabled on the Triggers -> Notifications page.


Appendix Related Daemons
-------------------------------------------------------------------------------

============  ===============================================================
Type          Name
============  ===============================================================
Notification  zenactiond
============  ===============================================================
