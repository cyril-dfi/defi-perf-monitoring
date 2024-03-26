from config import *
from mav_helper import *

MavHelper = MavHelper()

def main():
    MavHelper.get_pools(argument.network, 'maverick')

    for owner_address in ADDRESSES:
        MavHelper.get_latest_data(owner_address, argument.network, 'maverick')

if __name__ == "__main__":
    main()
