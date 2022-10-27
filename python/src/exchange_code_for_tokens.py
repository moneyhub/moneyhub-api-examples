from config import *
import utils
import argparse

parser = argparse.ArgumentParser(description='Get AIS authorisation URL')
parser.add_argument("-s", "--state", default="foo", help="The state value")
parser.add_argument("-n", "--nonce", default="bar", help="The nonce value")
parser.add_argument("-c", "--code", help="The code to exchange tokens for")
parser.add_argument("-i", "--id_token", help="The code to exchange tokens for")
args = parser.parse_args()
identity_server = config["identity_service_url"]

utils.verify_id_token(config=config, id_token=args.id_token, nonce=args.nonce)
tokens = utils.exchange_code_for_tokens(config, args.nonce, args.id_token, args.code)

print(tokens)