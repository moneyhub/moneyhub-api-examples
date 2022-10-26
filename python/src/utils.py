import time
import random
import string
import requests
import jwt, jwcrypto.jwk as jwk, datetime
from datetime import datetime, timedelta

def generate_jti():
  letters = string.ascii_lowercase
  return "".join(random.choice(letters) for i in range(32))

def get_jwt(payload, private_key, headers=None):
  return jwt.encode(
    payload,
    private_key.export_to_pem(private_key=True, password=None), 
    algorithm="RS256",
    headers=headers
  )

def get_common_claims():
  iat = datetime.now()
  exp = datetime.now() + timedelta(hours=1)

  return {
    "iat": time.mktime(iat.timetuple()),
    "exp": time.mktime(exp.timetuple()),
    "jti": generate_jti(),
  }

def get_request_object(config, payload):
  private_key = get_private_key(config)
  return get_jwt(payload, private_key, {
    "typ": "oauth-authz-req+jwt",
    "alg": "RS256",
    "kid": private_key["kid"]
  })

def get_client_assertion(config, scope):
  client_id = config["client"]["client_id"]
  identity_server = config["identity_service_url"]

  private_key = get_private_key(config)

  payload = { 
    "iss": client_id,
    "sub": client_id,
    "aud": "{}/oidc/token".format(identity_server),
    "scope": scope,
    **get_common_claims()
  }

  return get_jwt(payload, private_key)

def get_private_key(config):
  return jwk.JWK(**config["client"]["keys"][0])

def get_client_credentials_token(config, scope, user_id=None):
  identity_server = config["identity_service_url"]

  client_assertion = get_client_assertion(config=config, scope=scope)
  params = {
    "scope": scope,
    "grant_type": "client_credentials",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": client_assertion,
    "sub": user_id,
  }

  headers = {
    "Content-Type": "application/x-www-form-urlencoded",
  }

  res = requests.post("{}/oidc/token".format(identity_server), data=params, headers=headers)
  return res.json()

def create_payee(config, name, sort_code, account_number):
  identity_server = config["identity_service_url"]
  token = get_client_credentials_token(config, "payee:create")
  
  data = {
    "accountNumber": account_number,
    "sortCode": sort_code,
    "name": name
  }

  headers = {
    "Authorization": "Bearer {}".format(token["access_token"]),
  }

  res = requests.post("{}/payees".format(identity_server), json=data, headers=headers)
  return res.json()

def post_request_object(config, payload):
  identity_server = config["identity_service_url"]
  request_object = get_request_object(config, payload)

  headers = {
    "Content-Type": "application/jws"
  }

  res = requests.post("{}/request".format(identity_server), data="{}".format(request_object), headers=headers)
  return res.text