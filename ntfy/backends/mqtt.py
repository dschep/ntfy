import json
import logging
import paho.mqtt.publish as publish

def notify(title, message, **kwargs):
    """
    Publishes a notification to an MQTT topic.
    """
    hostname = kwargs.get("hostname")
    topic = kwargs.get("topic")

    if not hostname or not topic:
        logging.error("MQTT backend requires 'hostname' and 'topic' parameters in the configuration.")
        return

    port = int(kwargs.get("port", 1883))
    qos = int(kwargs.get("qos", 1))
    retcode = kwargs.get("retcode")
    username = kwargs.get("username")
    password = kwargs.get("password")

    payload = json.dumps({
        "title": title,
        "message": message,
        "retcode": retcode
    })

    auth = None
    if username:
        auth = {'username': username, 'password': password}

    try:
        publish.single(
            topic=topic,
            payload=payload,
            hostname=hostname,
            port=port,
            qos=qos,
            auth=auth
        )
    except Exception as e:
        logging.error("Failed to publish MQTT message: %s", e)