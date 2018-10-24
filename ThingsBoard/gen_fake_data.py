import os
import time

while 1:
	os.system('mosquitto_pub -h 192.168.1.198 -t "v1/devices/me/telemetry" -u "HPCC_Light_Temp_Humi" -P "" -m "{\"temperature\":30, \"light\":1, \"humidity\":60}"')
	os.system('mosquitto_pub -h 192.168.1.198 -t "v1/devices/me/telemetry" -u "HPCC_Motion_Led" -P "" -m "{\"motion\":1}"')
	time.sleep(5)

	os.system('mosquitto_pub -h 192.168.1.198 -t "v1/devices/me/telemetry" -u "HPCC_Light_Temp_Humi" -P "" -m "{\"temperature\":32, \"light\":0, \"humidity\":62}"')
	os.system('mosquitto_pub -h 192.168.1.198 -t "v1/devices/me/telemetry" -u "HPCC_Motion_Led" -P "" -m "{\"motion\":1}"')
	time.sleep(5)

	os.system('mosquitto_pub -h 192.168.1.198 -t "v1/devices/me/telemetry" -u "HPCC_Light_Temp_Humi" -P "" -m "{\"temperature\":35, \"light\":1, \"humidity\":65}"')
	os.system('mosquitto_pub -h 192.168.1.198 -t "v1/devices/me/telemetry" -u "HPCC_Motion_Led" -P "" -m "{\"motion\":0}"')
	time.sleep(5)

	os.system('mosquitto_pub -h 192.168.1.198 -t "v1/devices/me/telemetry" -u "HPCC_Light_Temp_Humi" -P "" -m "{\"temperature\":40, \"light\":1, \"humidity\":70}"')
	os.system('mosquitto_pub -h 192.168.1.198 -t "v1/devices/me/telemetry" -u "HPCC_Motion_Led" -P "" -m "{\"motion\":0}"')
	time.sleep(5)

