from config import *
import utils
import argparse

parser = argparse.ArgumentParser(description='Get client credentials token from Moneyhub')
parser.add_argument("-s", "--scope", default="user:read", help="The scope value you want a token for")
parser.add_argument("-u", "--userId", help="The userId you want the token to be scoped to")
args = parser.parse_args()

token = utils.get_client_credentials_token(config, args.scope, args.userId)

print(token)