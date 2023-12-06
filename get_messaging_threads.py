
def get_messaging_threads():
    from get_token import get_token
    import requests
    url = 'https://api.allegro.pl/messaging/threads'
# Set up the headers with the token and the required Accept header
    headers = {
        'Authorization': f'Bearer {get_token()}',
        'Accept': 'application/vnd.allegro.public.v1+json'
    }

    # Make the GET request
    response = requests.get(
        f'{url}',
        headers=headers
    )

    # Check if the request was successful
    if response.ok:
        return response.json()
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")


print(get_messaging_threads())
