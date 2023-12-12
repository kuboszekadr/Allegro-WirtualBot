import os
import logging

from src.AppConfig import config

from src.endpoints.auth.Token import Token
from src.endpoints.messaging.Threads import Threads
from src.endpoints.messaging.Thread import Thread

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='.logs',
    filemode='w'
)

logging.info('Starting Allegro Assistant')

token = Token(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    device_code=os.getenv('DEVICE_CODE')
)

threads = Threads(token)
threads.get()

for thread in threads.threads:
    thread.get_messages()
    last_msg = thread.get_last_message_from_user(config.allegro.user_name)

    if last_msg is None:
        logging.info(f"Sending message to thread: {thread.id}")
        thread.send_message("""Dzień dobry, 
                            bardzo dziękujemy zainteresowanie nasza aukcja i kontakt z nami. Nasz asystent w niedługim czasie wróci z odpowiedzią na Twoje pytanie. Pozdrawiamy serdecznie!""")
        logging.info(f"Sending message to thread: {thread.id} - DONE")

logging.info('Allegro Assistant finished')