from decimal import Decimal

import requests
from .models import CoinList


# To run in terminal:
# 1. Move to root directory of project
# 2. Run command: python manage.py shell
# 3. In shell, import function: from <AppName>.coin_api import update_coin_list
# 4. In shell, run function: update_coin_list()
def update_coin_list():
    rqst_json = requests.get('https://api.coingecko.com/api/v3/coins/list').json()
    for coin in rqst_json:
        if not CoinList.objects.filter(coin_id=coin['id']).exists():
            newcoin = CoinList(coin_id=coin['id'], coin_symbol=coin['symbol'], coin_name=coin['name'])
            newcoin.save()


# Get prices and calculate gain/loss for a list of coins
def fetch_prices(coins):
    coin_ids = ''
    for coin in coins:
        coin_ids += coin.coin_api_id + '%2C'
    rqst = f'https://api.coingecko.com/api/v3/simple/price?ids={coin_ids}&vs_currencies=cad'
    rqst_json = requests.get(rqst).json()
    for coin in coins:
        price = -1
        if 'cad' in rqst_json[coin.coin_api_id]:
            price = rqst_json[coin.coin_api_id]['cad']
        coin.current_price = Decimal(price)
        if not coin.total_cost <= 0:
            coin.gain_loss = ((coin.balance * coin.current_price - coin.total_cost) / coin.total_cost) * 100
        else:
            coin.gain_loss = 0
