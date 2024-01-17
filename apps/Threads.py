import logging
from time import sleep

import sys
import os

sys.path.append(os.getcwd())


from datetime import datetime as dt
from tqdm import tqdm
from src.AppConfig import config

from src.endpoints.auth.Token import Token
from src.endpoints.messaging.Threads import Threads


logging.info('Starting Allegro Assistant')
log_file = dt.now().strftime("%Y-%m-%d.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=f'logs/{log_file}.log',
    filemode='w'
)

user = config.allegro.user_name
token = Token(
    client_id=config.allegro.client_id,
    client_secret=config.allegro.client_secret
    )

threads = Threads(token)
threads.get(cutoff=2)

sent = 0

for thread in tqdm(threads.threads):
    thread.get_messages()

    if thread.requires_answer(user):
        logging.info(f"Sending message to thread: {thread.id}")
        thread.send_message("""Dzień dobry, 
                            bardzo dziękujemy zainteresowanie nasza aukcja i kontakt z nami. Nasz asystent w niedługim czasie wróci z odpowiedzią na Twoje pytanie. Pozdrawiamy serdecznie!""")
        logging.info(f"Sending message to thread: {thread.id} - DONE")
        sent += 1
        sleep(1)

logging.info(f'Allegro Assistant finished, sent {sent} msgs')
