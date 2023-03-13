from config import *
import utils
import argparse
import json

parser = argparse.ArgumentParser(description='Get AIS PAR authorisation URL')
parser.add_argument("-s", "--state", default="foo", help="The state value")
parser.add_argument("-n", "--nonce", default="bar", help="The nonce value")
args = parser.parse_args()
identity_server = config["identity_service_url"]

user = utils.register_user(config)

client_id = config["client"]["client_id"]
params = {
  "client_id": client_id,
  "scope": "openid id:test",
  "state": args.state,
  "nonce": args.nonce,
  "redirect_uri": config["client"]["redirect_uri"],
  "response_type": config["client"]["response_type"],
  "claims": json.dumps({
    "id_token": {
      "sub": {
        "essential": True,
        "value": user["userId"]
      },
      "mh:con_id": {
        "essential": True
      },
    }
  }),
}

par_response = utils.post_pushed_authorisation_url(config, params)

print("{}/oidc/auth?request_uri={}".format(identity_server, par_response["request_uri"]))