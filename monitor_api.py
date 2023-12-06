def monitor_api(check_interval=10):
    from get_disputes import get_disputes
    from post_auto_message import post_auto_message
    import time

    print(f"{get_disputes()} Monitoring disputes for changes...")
    last_data = None

    while True:
        current_data = get_disputes()
        print(f"Monitoring for changes...")

        if last_data is not None and current_data != last_data:
            print(f"Change detected in API at Disputes")
            post_auto_message()
            print(f"Auto message sent!")

        last_data = current_data
        time.sleep(check_interval)
