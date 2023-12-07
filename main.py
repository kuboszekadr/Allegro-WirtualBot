import logging
from src import get_messaging_threads
from src import post_auto_message

#     if last_data is not None and current_data != last_data:

logging.info(f"Monitoring disputes for changes...")
last_data = None
current_data = get_messaging_threads()
thread_id = current_data.get('threads')[0].get('id')
post_auto_message(thread_id)
logging.info(f"Auto message sent!")

#     last_data = current_data

print(get_messaging_threads())
