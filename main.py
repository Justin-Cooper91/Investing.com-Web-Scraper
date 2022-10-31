import pandas as pd
import requests
from bs4 import BeautifulSoup
import schedule
import time

def scraper(t):
    url = 'https://www.investing.com/equities/top-stock-gainers'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', {'class': 'genTbl closedTbl elpTbl elp25 crossRatesTbl'})
    headers = []
    for i in table.find_all('th'):
        title = i.text.strip()
        headers.append(title)
    df = pd.DataFrame(columns=headers)
    for row in table.find_all('tr')[1:]:
        data = row.find_all('td')
        row_data = [td.text.strip() for td in data]
        length = len(df)
        df.loc[length] = row_data
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    data = df.to_json(orient='values')
    data = df.to_json('./gains.json', orient='values')
    print(data)
    url = 'https://www.investing.com/equities/top-stock-losers'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', {'class': 'genTbl closedTbl elpTbl elp25 crossRatesTbl'})
    headers = []
    for i in table.find_all('th'):
        title = i.text.strip()
        headers.append(title)
    df = pd.DataFrame(columns=headers)
    for row in table.find_all('tr')[1:]:
        data = row.find_all('td')
        row_data = [td.text.strip() for td in data]
        length = len(df)
        df.loc[length] = row_data
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    data = df.to_json(orient='values')
    data = df.to_json('./losses.json', orient='values')
    print(data)
    return

schedule.every().day.at("09:33").do(scraper,'It is 09:33')
while True:
    schedule.run_pending()
    time.sleep(60)

