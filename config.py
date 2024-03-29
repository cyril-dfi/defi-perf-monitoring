import argparse
from datetime import datetime, timezone
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ADDRESSES = os.environ.get('ADDRESSES').split(',')
THEGRAPH_KEY = os.environ.get('THEGRAPH_KEY')


supported_networks = [
  'ethereum', 
  'zksync', 
  'bnb', 
  'base',
]

MAV_CHAIN_ID = {
    "ethereum": 1,
    'bnb': 56,
    "zksync": 324,
    "base": 8453
}

THEGRAPH_URLS = {
     "uniswapv3": {
          "ethereum": f'https://gateway-arbitrum.network.thegraph.com/api/{THEGRAPH_KEY}/subgraphs/id/HUZDsRpEVP2AvzDCyzDHtdc64dyDxx8FQjzsmqSg4H3B'
     }
}

START_TIME = datetime.now(timezone.utc)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Argument parsing setup
# TODO: Add error if network / chain is not supported
def setup_parser():
     parser = argparse.ArgumentParser(description = "You need to specify the network (-n)")
     parser.add_argument("-n", "--network", help = "Network or chain (choose between ethereum, zksync, bnb and base)", required = True)
     parser.add_argument("-a", "--app", help = "App/Protocol/Dex used (choose between maverick and uniswapv3)", required = True)
     return parser.parse_args()

argument = setup_parser()

def log_argument(argument_name, argument_value):
    logging.info(f"You have used '-{argument_name[0]}' or '--{argument_name}' with argument: {argument_value}")

log_argument('network', argument.network)
log_argument('app', argument.app)

