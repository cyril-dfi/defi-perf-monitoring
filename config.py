import argparse
from datetime import datetime, timezone
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ADDRESSES = os.environ.get('ADDRESSES').split(',')

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

START_TIME = datetime.now(timezone.utc)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Argument parsing setup
# TODO: Add error if network / chain is not supported
def setup_parser():
     parser = argparse.ArgumentParser(description = "You need to specify the network (-n)")
     parser.add_argument("-n", "--network", help = "Network or chain (choose between ethereum, zksync, bnb or base)", required = True)
     return parser.parse_args()

argument = setup_parser()

def log_argument(argument_name, argument_value):
    logging.info(f"You have used '-{argument_name[0]}' or '--{argument_name}' with argument: {argument_value}")

log_argument('network', argument.network)

