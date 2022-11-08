from config import *
import utils
import argparse

parser = argparse.ArgumentParser(description='Get PIS authorisation URL that creates a payee')
parser.add_argument("-s", "--state", default="foo", help="The state value")
parser.add_argument("-n", "--nonce", default="bar", help="The nonce value")
args = parser.parse_args()

identity_server = config["identity_service_url"]

payee = utils.create_payee(config, name="payee name", sort_code="123456", account_number="12345678")
payee_id = payee["data"]["id"]

client_id = config["client"]["client_id"]
params = {
  "client_id": client_id,
  "scope": "openid id:test payment",
  "state": args.state,
  "nonce": args.nonce,
  "redirect_uri": config["client"]["redirect_uri"],
  "response_type": "code id_token",
  "claims": {
    "id_token": {
      "mh:con_id": {
        "essential": True
      },
      "mh:payment": {
        "essential": True,
        "value": {
          "amount": 100,
          "payeeRef": "reference",
          "payerRef": "reference",
          "payeeId": payee_id,
        }
      }
    }
  },
  "aud": "{}/oidc".format(identity_server),
  "iss": client_id,
  **utils.get_common_claims()
}

request_uri = utils.post_request_object(config, params)
print("{}/oidc/auth?request_uri={}".format(identity_server, request_uri))