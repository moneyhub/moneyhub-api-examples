from config import *
import utils
import argparse
import json

parser = argparse.ArgumentParser(description='Get AIS authorisation URL')
parser.add_argument("-u", "--user_id", help="The user ID to get accounts for")
args = parser.parse_args()
identity_server = config["identity_service_url"]

accounts = utils.get_accounts(config, args.user_id)

print(json.dumps(accounts, indent=2))