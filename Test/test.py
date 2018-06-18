# import paho.mqtt.client as mqtt
# from influxdb import InfluxDBClient
# import ast
# import json
# import threading
# from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
# from kombu.utils.compat import nested
# import time
#
# BROKER_CLOUD = "localhost"
#
# producer_connection = Connection(BROKER_CLOUD)
# consumer_connection = Connection(BROKER_CLOUD)
# MODE = "PUSH" # PUSH or PULL
#
# exchange = Exchange("test", type="direct")
#
# def handle_notification(body, message):
#     # receive list items
#     print('Receive message from Collector')
#     print (body)
#     time.sleep(10)
#
# test = Queue(name='test', exchange=exchange,
#                          routing_key='test')
#
# while 1:
#     try:
#         consumer_connection.ensure_connection(max_retries=1)
#         with nested(Consumer(consumer_connection, queues=test,
#                              callbacks=[handle_notification], no_ack=True)):
#             while True:
#                 consumer_connection.drain_events()
#     except (ConnectionRefusedError, exceptions.OperationalError):
#         print('Connection lost')
#     except consumer_connection.connection_errors:
#         print('Connection error')


# #!/usr/bin/python3
#
# import _thread
# import time
#
# # count = 0
# str = "a"
#
# # Define a function for the thread
# def print_a():
#     while (1):
#         global str
#         time.sleep(1)
#         print (str)
#
#
# def update():
#     global str
#     str = "b"
#
# # Create two threads as follows
# try:
#     _thread.start_new_thread(print_a, () )
#
# except:
#     print ("Error: unable to start thread")
#
#
#
# time.sleep(10)
# print ("sleep 1")
#
# _thread.start_new_thread(update,() )
#
# time.sleep(10)
# print ("sleep 2")


#!/usr/bin/env python3
import json
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5008
BUFFER_SIZE = 1024
MESSAGE = '{"rule" : "2fd90a58-ae0f-4400-b561-9f0978fb7184-Temperature-Temperature<20", "action":"Alert"}'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE.encode())
data = s.recv(BUFFER_SIZE)
s.close()

print ("received data:", data)
