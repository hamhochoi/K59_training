# IOT Platform OpenHAB và kịch bản triển khai
    - Hệ thống được cài đặt trên zone_3 (phòng làm việc của sinh viên). 
    - Hệ thống gồm 2 Fog Node và 1 Pi3 cài đặt OpenHAB để quản lý các Fog Node.
    
## Kịch bản cài đặt
  - Hệ thống gồm có: 
    - 02 Arduino
    - 02 Esp 8266
    - 01 Raspberry Pi 3 cài OpenHAB
    - 01 cảm biến chuyển động
    - 01 cảm biến ánh sáng
    - 01 cảm biến nhiệt ẩm
    - 03 đèn LED: vàng, đỏ, xanh
    - Chương trình điều khiển thực hiện kịch bản bật tắt đèn khi có chuyển động đi qua.
    
  - Kịch bản sử dụng
    - Khi cảm biến chuyển động phát hiện có chuyển động, chương trình điều khiển sẽ thực hiện bật một trong 3 đèn: đèn xanh khi cường độ sáng lớn (tương ứng giá trị của cảm biến ánh sáng >= 600); đèn đỏ khi cường độ sáng trung bình (giá trị >=500, <600); đèn vàng khi cường độ sáng yếu (giá trị <500)
    
## Cài đặt hệ thống
### Arduino
    - Arduino được sử dụng để nhận các giá trị từ cảm biến và đẩy dữ liệu cho ESP 8266 thông qua các chân RX, TX. 
### ESP 8266
    - Broker: cài docker image mqtt trên Pi 3 làm một broker tại địa chỉ IP 192.168.60.197
        - docker run -itd --name mosquitto -p 1883:1883 haiquan5396/mqtt 
    - ESP 8266 chuyển dữ liệu lên/nhận lệnh từ broker thông qua giao thức MQTT (Mosquito) vào các topic publish, subscribe.  
      
### OpenHAB        
    - IOT Platform OpenHAB được cài đặt trên Pi 3 nhận dữ liệu/gửi lệnh cho ESP 8266 thông qua các topic subscribe, publish tương ứng. 
    - Cài đặt MQTT Binding; JSON Binding trên OpenHAB PaperUI.
    - Cầu hình broker cho MQTT binding bằng cách thêm 1 file default.service vào thư mục service của OpenHAB:
``` 
    mybroker.url=tcp://192.168.60.197:1883
```
    Khi này, các gói tin MQTT sẽ được chuyển đến broker 192.168.60.197 cổng 1883.
    - Các Items có trong hệ thống 
        - 3 đèn tương ứng với 3 Switch (Switch 1 - đèn vàn; Switch 2 - đèn đỏ; Switch 3 - đèn xanh). Mỗi đèn khi được bật/tắt sẽ gửi về 1 topic trên broker 192.168.60.197 (topic publish: zone_3/box_1/led).
        - Cảm biến chuyển động (topic subscribe: zone_3/box_1/motion/id_1).
        - Cảm biến ánh sáng (topic subscribe: zone_3/box_1/light/id_1
        - Cảm biến nhiệt độ, độ ẩm (topic subscribe: zone_3/box_1/temp/id_1).
```
Switch Switch1 <light> {mqtt=">[mybroker:zone_3/box_1/led:command:ON:{\"vang\"\\:\"ON\"}],>[mybroker:zone_3/box_1                                                                                                               /led:command:OFF:{\"vang\"\\:\"OFF\"}]"}

Switch Switch2 <light> {mqtt=">[mybroker:zone_3/box_1/led:command:ON:{\"do\"\\:\"ON\"}],>[mybroker:zone_3/box_1/led:command:OFF:                                                                                         {\"do\"\\:\"OFF\"}]"}

Switch Switch3 <light> {mqtt=">[mybroker:zone_3/box_1/led:command:ON:{\"xanh\"\\:\"ON\"}],>[mybroker:zone_3/box_1                                                                                                         /led:command:OFF:{\"xanh\"\\:\"OFF\"}]"}

Number Temperature "Temperature: [%.1f oC]" <temperature> {mqtt="<[mybroker:zoner_3/box_1                                                                                                                               /temp/id_1:state:JSONPATH($.temperature)]"}

Number Humidity "Humidity: [%.1f ]" <humidity> {mqtt="<[mybroker:zoner_3/box_1/temp/id_1:state:JSONPATH($.humidity)]"}

Number Motion "Motion: [ %d ]" <motion> {mqtt="<[mybroker:zone_3/box_1/motion/id_1:state:JSONPATH($.motion)]"}

Number Light "Light: [%d ]" <light> {mqtt="<[mybroker:zoner_3/box_1/light/id_1:state:JSONPATH($.light)]"}
```
    - Chương trình điều khiển đọc giá trị trả về từ cảm biến ánh sáng trên broker và ra lệnh cho OpenHAB bật các đèn tương ứng theo kịch bản sử dụng bằng cách sử dụng API của OpenHAB.
```
from openhab import openHAB
import paho.mqtt.client as mqtt
import json
import time


base_url = 'http://localhost:8080/rest'
openhab = openHAB(base_url)

# fetch all items
items = openhab.fetch_all_items()
# print (items)

item1 = openhab.get_item("Switch1")
item2 = openhab.get_item("Switch2")
item3 = openhab.get_item("Switch3")

temp_item = openhab.get_item("Temperature")
light_item = openhab.get_item("Light")
light_state = light_item.state

topic_sub_sensor = "zone_3/box_1/motion/id_1"
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
	client.subscribe(topic_sub_sensor)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	global pre_motion
	
	mes = json.loads(str(msg.payload))
	mes = mes['motion']

	if (mes == 1 and pre_motion == 0):
		# pre_motion = mes
		light_state = light_item.state
		print (light_state)
		if (light_state == 0):				# LDRReading < 500
			item1.on()						# Bat den vang
			time.sleep(0.5)
			item2.off()
			time.sleep(0.5)
			item3.off()
			print ("Vang: ON, Do: OFF, Xanh: OFF")
		elif (light_state == 1):			# LDRReading >= 500 <600
			item1.off()
			time.sleep(0.5)
			item2.on()						# Bat den do
			time.sleep(0.5)
			item3.off()
			print ("Vang: OFF, Do: ON, Xanh: OFF")	
		elif (light_state == 2):			# LDRReading >= 600
			item1.off()
			time.sleep(0.5)
			item2.off()
			time.sleep(0.5)
			item3.on()						# Bat den xanh
			print ("Vang: OFF, Do: OFF, Xanh: ON")	
		else:
			print ("ERROR!")
			exit()

client = mqtt.Client()
pre_motion = 0
pre_temp = 0

client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.60.197", 1883, 60)
client.loop_forever()
```
        - Chương trình sử dụng thư viện paho mqtt để gửi, nhận dữ liệu với broker và thư viện Python-OpenHAB để gọi API của OpenHAB. Chương trình được lặp vô hạn, tại mỗi vòng lặp, các hàm on_connect và on_message subscribe dữ liệu từ broker và xử lý, ra lệnh cho OpenHAB qua API theo kịch bản sử dụng.
    
### Các giá trị trả về của cảm biến
    - Cảm biến chuyển động: Trả về 0 nếu không phát hiện chuyển động, trả về 1 nếu phát hiện chuyển động
    - Cảm biến ánh sáng: Trả về giá trị 0-1023, gía trị càng lớn tức cường độ ánh sáng càng lớn.
    - Cảm biến nhiệt độ độ ẩm: Trả về 2 giá trị nhiệt độ (độ C) và độ ẩm (%)
    - 03 đèn LED: vàng, đỏ, xanh.

### NOTE:
    - Cách lắp mạch, mã nguồn của Arduino và ESP 8266 có trong file đính kèm.
    
