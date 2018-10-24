# import asyncio
# import paho.mqtt.client as mqtt


# # async def factorial(name, number):
# #     f = 1
# #     for i in range(2, number+1):
# #         print("Task %s: Compute factorial(%s)..." % (name, i))
# #         await asyncio.sleep(1)
# #         f *= i
# #     print("Task %s: factorial(%s) = %s" % (name, number, f))

# # loop = asyncio.get_event_loop()
# # loop.run_until_complete(asyncio.gather(
# #     factorial("A", 2),
# #     factorial("B", 3),
# #     factorial("C", 4),
# # ))
# # loop.close()

# async def process_msg(msg):
# 	for i in range(100):
# 		if (i%10 == 0):
# 			print (i)


# async def handle_init(client, userdata, msg):
# 	print ("handle message")
# 	await process_msg(msg)
# 	# loop = asyncio.get_event_loop()
# 	# loop.create_task(process_msg(msg))
	

# # def on_connect(client, userdata, flags, rc):
# # 	print ("receive message")
# # 	clientMQTT.subscribe("test")
# # 	clientMQTT.message_callback_add("test", handle_init)

# clientMQTT = mqtt.Client()
# clientMQTT.connect("localhost")
# # clientMQTT.on_connect = on_connect
# clientMQTT.subscribe("test")
# clientMQTT.message_callback_add("test", handle_init)

# def connect():
# 	while (1):
# 		clientMQTT.loop_start()		
# 		# print ("receive message")
		
# 		# clientMQTT.loop_forever()
# 		clientMQTT.loop_stop()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(connect())
# loop.close()
# # connect()

# # self.clientMQTT.loop_start()
# # clientMQTT.publish('test', json.dumps(message))



import asyncio
 
 
def foo2(delay):
	for i in range(100000000):
		if (i%10000000 == 0):
			print (i)

async def foo(delay):
	# await asyncio.sleep(delay)
	await foo2(delay)
 
 
def stopper(loop):
    loop.stop()
 
 
loop = asyncio.get_event_loop()
 
# Schedule a call to foo()
loop.create_task(foo(0.5))
loop.create_task(foo(1))
loop.call_later(12, stopper, loop)
 
# Block until loop.stop() is called()
loop.run_forever()
loop.close()