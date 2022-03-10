from telethon import TelegramClient
from decouple import config

api_id = config('api_id')
api_hash = config('api_hash')
phone = config('phone')


def send_message_to(user, file_name):
    api_id = config.api_id
    api_hash = config.api_hash
    phone = config.phone
    client = TelegramClient('session_name', api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
    
        client.send_code_request(phone)
        
        # signing in the client
        client.sign_in(phone, input('Enter the code: '))

    client.send_file(user, str(file_name)+".pdf", "Save this id to ask for later for your file "+ file_name)
    client.disconnect()