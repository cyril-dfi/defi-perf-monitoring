from config import *
import requests
import json

class TheGraphHelper():
    def __init__(self):
        if argument.app == 'uniswapv3':
            self.api_url = THEGRAPH_URLS[argument.app][argument.network]

    def get_data(self, query):
        r = requests.post(self.api_url, json={'query': query})
        if r.status_code == 200:
            result = json.loads(r.text)
            return result
        else:
            logging.error(f"Error with status code {r.status_code}")
            return None
