def monitor_api():
    from get_messaging_threads import get_messaging_threads
    from post_auto_message import post_auto_message
    import time
    print(f"Monitoring disputes for changes...")
    last_data = None
    current_data = get_messaging_threads()
    thread_id = current_data.get('threads')[0].get('id')
    post_auto_message(thread_id)
    print(f"Auto message sent!")

    # while True:
    #     current_data = get_messaging_threads()
    #     print(f"Monitoring for changes...")

    #     if last_data is not None and current_data != last_data:
    #         print(f"Change detected in API at Disputes")
    #         thread_id = current_data.get('threads')[0].get('id')
    #         post_auto_message(thread_id)
    #         print(f"Auto message sent!")

    #     last_data = current_data
    #     time.sleep(check_interval)


monitor_api()
