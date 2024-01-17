import logging

from time import sleep

import sys
import os
sys.path.append(os.getcwd())


from datetime import datetime as dt
from tqdm import tqdm
from src.AppConfig import config

from src.endpoints.auth.Token import Token
from src.endpoints.disputes.Disputes import Disputes


logging.info('Starting Allegro Assistant')
log_file = dt.now().strftime("%Y-%m-%d.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=f'logs/{log_file}.log',
    filemode='w'
)

token = Token(
    client_id=config.allegro.client_id,
    client_secret=config.allegro.client_secret,)

user = config.allegro.user_name

disputes = Disputes(token)
disputes.get()

sent = 0

for dispute in tqdm(disputes.disputes):
    logging.info(f"Sending message to dispute: {dispute.id}")
    dispute.send_message("""Dzień dobry, 
                        dziękujemy za kontakt. Nasz asystent w niedługim czasie wróci z odpowiedzią. Pozdrawiamy serdecznie!""")
    logging.info(f"Sending message to dispute: {dispute.id} - DONE")
    sent += 1
    sleep(1)

logging.info(
    f'Allegro Assistant finished, sent {sent} msgs')
