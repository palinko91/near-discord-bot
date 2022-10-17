from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()
api_key = os.getenv('COINMARKETCAP_API_KEY')

url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
parameters = {
  'id': '6535',
  'aux':
  'max_supply,circulating_supply,total_supply,market_cap_by_total_supply'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api_key,
}

session = Session()
session.headers.update(headers)

def get_data():
  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    near_data = {
      'timestamp':data['data']['6535']['last_updated'],
      'total_supply':data['data']['6535']['total_supply'],
      'circulating_supply':data['data']['6535']['circulating_supply'],
      'price':data['data']['6535']['quote']['USD']['price'],
      'price_change_24h':data['data']['6535']['quote']['USD'][
      'percent_change_24h'],
      'volume_24h':data['data']['6535']['quote']['USD']['volume_24h'],
      'volume_change_24h':data['data']['6535']['quote']['USD'][
      'volume_change_24h'],
      'market_cap':data['data']['6535']['quote']['USD']['market_cap']
    }
    return near_data

  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

