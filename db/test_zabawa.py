import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def get_bitcoin_data(start_date, end_date):
    url = f'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start={start_date}&end={end_date}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'class': 'cmc-table'})
    rows = table.find_all('tr')[1:]  # Skip header row

    data = []
    for row in rows:
        cols = row.find_all('td')
        date_str = cols[0].text
        date = datetime.strptime(date_str, '%b %d, %Y').strftime('%Y-%m-%d')
        close_price = cols[4].text.replace(',', '')
        data.append([date, close_price])

    return pd.DataFrame(data, columns=['Date', 'Close'])


# Example usage
start_date = '20200101'  # Format: YYYYMMDD
end_date = '20211231'
bitcoin_data = get_bitcoin_data(start_date, end_date)
print(bitcoin_data)
