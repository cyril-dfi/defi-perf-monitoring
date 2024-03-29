from config import *
import logging
from helpers.mariadb_helper import MariaDBHelper
import sys
import requests

MariaDBHelper = MariaDBHelper()

class MavHelper():
     def __init__(self):
          self.chain_id = MAV_CHAIN_ID[argument.network]

     def get_pool_data(self):
          self.pool_api_url = f"https://api.mav.xyz/api/v4/pools/{self.chain_id}"
          pool_data = requests.get(self.pool_api_url).json()
          return pool_data

     def get_user_data(self, owner_address):
          user_api_url = f"https://api.mav.xyz/api/v4/user/{owner_address}/{self.chain_id}"
          logging.info(f"Calling {user_api_url}")
          user_data = requests.get(user_api_url).json()
          return user_data

     def get_pools(self):
          pool_data = self.get_pool_data()
          for pool in pool_data['pools']:
               pool_data = {'address': pool["id"], 'name': pool["name"]}
               pool_token_data = [
                    {'address': pool["tokenA"]["address"], 'symbol': pool["tokenA"]["symbol"]},
                    {'address': pool["tokenB"]["address"], 'symbol': pool["tokenB"]["symbol"]},
               ]
               MariaDBHelper.insert_pool(pool_data, pool_token_data, argument.network, argument.app)

     def split_pool_id(self, position):
          nb_char_nft_id = position['id'].find("0x", 2)
          nft_id = int(position['id'][:nb_char_nft_id-1],16) # The first characters of the "id" field correspond to the NFT ID
          pool_address = position['id'][nb_char_nft_id:] # The rest corresond to the pool address
          return nft_id, pool_address

     def get_latest_data(self, owner_address):
          user_data = self.get_user_data(owner_address)
          for position in user_data["user"]["positions"]:
               if position["balance"] > 0:
                    # Find the second instance of "0x"
                    nft_id, pool_address = self.split_pool_id(position)
                    position_data = {
                         'pool_address': pool_address, 
                         'nft_id': nft_id, 
                         'balance': position['balance'],
                         'token_balances': {
                              position["pool"]["tokenA"]["address"]: position["reserveA"],
                              position["pool"]["tokenB"]["address"]: position["reserveB"],
                         }
                    }
                    MariaDBHelper.insert_position(owner_address, position_data, argument.network, argument.app)
