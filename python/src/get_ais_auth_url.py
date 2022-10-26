from config import *
import utils
import argparse

parser = argparse.ArgumentParser(description='Get AIS authorisation URL')
parser.add_argument("-s", "--state", default="foo", help="The state value")
args = parser.parse_args()
identity_server = config["identity_service_url"]

client_id = config["client"]["client_id"]
params = {
  "client_id": client_id,
  "scope": "openid id:test",
  "state": args.state,
  "redirect_uri": config["client"]["redirect_uri"],
  "response_type": "code",
  "claims": {
    "id_token": {
      "sub": {
        "essential": True
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