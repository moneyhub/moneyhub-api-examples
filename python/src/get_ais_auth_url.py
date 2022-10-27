from config import *
import utils
import argparse

parser = argparse.ArgumentParser(description='Get AIS authorisation URL')
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
  "claims": {
    "id_token": {
      "sub": {
        "essential": True,
        "value": user["userId"]
      },
      "mh:con_id": {
        "essential": True
      },
    }
  },
  "iss": client_id,
  "aud": "{}/oidc".format(identity_server),
  **utils.get_common_claims()
}

request_object = utils.get_request_object(config, params)

print("{}/oidc/auth?request={}".format(identity_server, request_object))