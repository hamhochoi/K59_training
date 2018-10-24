import time
from sinchsms import SinchSMS


number = '+841626118018'
# number = '+841626630681'
message = "I love SMS!"
# client = SinchSMS("ce7ec38a-2ba2-47e8-aaf1-419a59809eca", "75jYmrdsG0aVAFUQu5AlIQ==")
client = SinchSMS("76e36416-cb7e-4637-81aa-d6b895650eb1", "6j58PMqzH0iEhMbjsWvvHQ==")
print("Sending '%s' to %s" % (message, number))
response = client.send_message(number, message)
message_id = response['messageId']
response = client.check_status(message_id)

while response['status'] != 'Successful':
    print(response['status'])
    time.sleep(1)
    response = client.check_status(message_id)
    print(response['status'])