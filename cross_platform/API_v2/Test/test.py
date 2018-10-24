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


# #!/usr/bin/env python3
# import json
# import socket
#
# TCP_IP = '127.0.0.1'
# TCP_PORT = 5008
# BUFFER_SIZE = 1024
# MESSAGE = '{"rule" : "2fd90a58-ae0f-4400-b561-9f0978fb7184-Temperature-Temperature<20", "action":"Alert"}'
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))
# s.send(MESSAGE.encode())
# data = s.recv(BUFFER_SIZE)
# s.close()
#
# print ("received data:", data)


#
# from multiprocessing import Process
# import time
#
#
# def f():
#     a = 10
#     print (a)
#     global a
#     b = 0
#     while b==0:
#         global b
#         g()
#     print (b)
#
#
# def g():
#     # print ("g")
#     # time.sleep(5)
#     # global a
#     # print (a)
#     global b
#     b = 1
#     print (b)
#
# def h():
#     global a
#     print (a)
#
# p1 = Process(target=f, args=())
# # p2 = Process(target=h, args=())
#
# p1.start()
# # p2.start()
#
# p1.join()
# p2.join()

# global a
# print (a)

#
# import threading
# import time
#
# a = 1
#
# def f():
#     global a
#     print (a)
#     a = 10
#
# def g():
#     print ("g")
#     # time.sleep(5)
#     global a
#     print (a)
#
# threads = []
#
# t = threading.Thread(target=f)
# threads.append(t)
# t.start()
#
# t2 = threading.Thread(target=g)
# threads.append(t2)
# t2.start()
#
# global a
# print (a)

import paho.mqtt.client as mqtt
import json
import os

def detect_motion(client, userdata, msg):
    message = json.loads(msg.payload.decode('utf-8'))
    # print (message)
    f = open("monitor_motion_sensor.txt", 'a')
    f.write(str(message)); f.write("\n")
    f.close()

    file_size = int(os.path.getsize("monitor_motion_sensor.txt"))
    if (file_size > 104857600): # 100 MB
        os.remove("monitor_motion_sensor.txt")


def on_connect(client, userdata, flags, rc):
    print("connect to Mosquitto")
    clientMQTT.subscribe('zone_3/box_1/motion/id_1')
    clientMQTT.message_callback_add('zone_3/box_1/motion/id_1', detect_motion)

def on_disconnect(client, userdata, rc):
    print ("disconnected!")


clientMQTT = mqtt.Client()
clientMQTT.connect("192.168.60.197")
clientMQTT.on_connect = on_connect
clientMQTT.disconnect = on_disconnect

clientMQTT.loop_forever()

