from config import *
import logging
from helpers.mariadb_helper import MariaDBHelper
from helpers.thegraph_helper import TheGraphHelper
import sys
import time
import requests
import json

MariaDBHelper = MariaDBHelper()
TheGraphHelper = TheGraphHelper()

class UniswapHelper():
    def __init__(self):
        pass
        # TheGraphHelper.api_url

    def get_latest_data(self, owner_address, network, app):
        pass
        # MariaDBHelper.insert_position(owner_address, position_data, network, app)

    def get_pools_query(self, last_pool_fetched):
        query = f"""{{
    pools(
        orderBy: createdAtTimestamp
        skip: {last_pool_fetched}
        first: 1000
    ) {{
        id
        token0 {{
            id
            symbol
        }}
        token1 {{
            id
            symbol
        }}
    }}
    }}"""
        return query

    def get_pools(self):
        last_pool_fetched = self.get_total_number_of_pools()
        logging.info(f"Uniswap v3 pools fetching - Starting from pool {last_pool_fetched}")
        done = False
        while not done:
            logging.info(f"Uniswap v3 pools fetching - Fetching pools {last_pool_fetched} to {last_pool_fetched+1000}")
            query = self.get_pools_query(last_pool_fetched)
            data = TheGraphHelper.get_data(query)
            pools = data['data']['pools']
            if pools:
                for pool in pools:
                    last_pool_fetched += 1
                    token0_symbol = pool["token0"]["symbol"]
                    token1_symbol = pool["token1"]["symbol"]
                    pool_data = {
                        'address': pool["id"],
                        'name': f"{token0_symbol}-{token1_symbol}",
                    }
                    pool_token_data = [
                        {'address': pool["token0"]["id"], 'symbol': token0_symbol},
                        {'address': pool["token1"]["id"], 'symbol': token1_symbol},
                    ]
                    MariaDBHelper.insert_pool(pool_data, pool_token_data, argument.network, 'uniswapv3')
            else:
                done = True
    
    def get_total_number_of_pools(self):
        query = f"""SELECT count(*)
        FROM pool
        INNER JOIN app_network ON pool.app_network_id = app_network.id
        INNER JOIN app ON app_network.app_id = app.id
        INNER JOIN network ON app_network.network_id = network.id
        WHERE app.name = '{argument.app}'
        AND network.name = '{argument.network}'
        """
        return MariaDBHelper.get_single_value_from_query(query)
        