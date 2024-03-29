from config import *
from mav_helper import *
from uniswap_helper import *

MavHelper = MavHelper()
UniswapHelper = UniswapHelper()

def main():
    if argument.app == 'maverick':
        MavHelper.get_pools()

        for owner_address in ADDRESSES:
            MavHelper.get_latest_data(owner_address)
    elif argument.app == 'uniswapv3':
        UniswapHelper.get_pools()
        pass

if __name__ == "__main__":
    main()
