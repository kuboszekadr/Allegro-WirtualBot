import os
import sys

from tqdm import tqdm

from src.auth.OAuth import OAuth
from src.messaging.Threads import Threads

user = os.environ['USER_NAME']
oauth = OAuth(
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET']
)
token = oauth.token[0]

threads = Threads(access_token=token)
threads_list = threads.get_recent_threads()

for thread in threads_list:
    msgs = threads.list_messages(thread['id'])
    root_last_msg = threads.get_last_message_from_user(msgs['messages'], user)

    if root_last_msg[0] is None:
        threads.send_message(
            thread['id'], 
            """Dzień dobry, 
            bardzo dziękujemy zainteresowanie naszą aukcją i kontakt z nami. Nasz asystent w niedługim czasie wróci z odpowiedzią na Twoje pytanie. 
            Pozdrawiamy serdecznie!
            """
            )
