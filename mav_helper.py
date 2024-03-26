from config import *
import logging
from mysql_helper import MySQLHelper
import sys
import requests
sys.set_int_max_str_digits(0)

MySQLHelper = MySQLHelper()

class MavHelper():
     def __init__(self):
          self.chain_id = MAV_CHAIN_ID[argument.network]

     def get_pools(self, network, app):
          pool_api_url = f"https://api.mav.xyz/api/v4/pools/{self.chain_id}"
          pool_api_url_data = requests.get(pool_api_url).json()
          for pool in pool_api_url_data['pools']:
               pool_data = {'address': pool["id"], 'name': pool["name"]}
               pool_token_data = [
                    {'address': pool["tokenA"]["address"], 'symbol': pool["tokenA"]["symbol"]},
                    {'address': pool["tokenB"]["address"], 'symbol': pool["tokenB"]["symbol"]},
               ]
               MySQLHelper.insert_pool(pool_data, pool_token_data, network, app)


     def get_latest_data(self, owner_address, network, app):
          user_api_url = f"https://api.mav.xyz/api/v4/user/{owner_address}/{self.chain_id}"
          logging.info(f"Calling {user_api_url}")
          user_api_data = requests.get(user_api_url).json()
          for position in user_api_data["user"]["positions"]:
               if position["balance"] > 0:
                    # Find the second instance of "0x"
                    nb_char_nft_id = position['id'].find("0x", 2)
                    nft_id = int(position['id'][:nb_char_nft_id-1],16) # The first characters of the "id" field correspond to the NFT ID
                    pool_address = position['id'][nb_char_nft_id:] # The rest corresond to the pool address
                    position_data = {
                         'pool_address': pool_address, 
                         'nft_id': nft_id, 
                         'balance': position['balance'],
                         'token_balances': {
                              position["pool"]["tokenA"]["address"]: position["reserveA"],
                              position["pool"]["tokenB"]["address"]: position["reserveB"],
                         }
                    }
                    MySQLHelper.insert_position(owner_address, position_data, network, app)
