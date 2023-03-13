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

def get_client_assertion(config):
  client_id = config["client"]["client_id"]
  identity_server = config["identity_service_url"]

  private_key = get_private_key(config)

  payload = { 
    "iss": client_id,
    "sub": client_id,
    "aud": "{}/oidc/token".format(identity_server),
    **get_common_claims()
  }

  return get_jwt(payload, private_key)

def get_private_key(config):
  return jwk.JWK(**config["client"]["keys"][0])

def get_client_credentials_token(config, scope, user_id=None):
  identity_server = config["identity_service_url"]

  client_assertion = get_client_assertion(config=config)
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

def register_user(config):
  identity_server = config["identity_service_url"]
  token = get_client_credentials_token(config, "user:create")

  headers = {
    "Authorization": "Bearer {}".format(token["access_token"])
  }

  res = requests.post("{}/users".format(identity_server), json={}, headers=headers)
  return res.json()

def exchange_code_for_tokens(config, nonce, id_token, code):
  identity_server = config["identity_service_url"]
  
  client_assertion = get_client_assertion(config=config)

  params = {
    "grant_type": "authorization_code",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": client_assertion,
    "redirect_uri": config["client"]["redirect_uri"],
    "code": code,
  }

  headers = {
    "Content-Type": "application/x-www-form-urlencoded"
  }

  res = requests.post("{}/oidc/token".format(identity_server), data=params, headers=headers)
  return res.json()

def get_accounts(config, user_id):
  api_url = config["resource_server_url"]
  token = get_client_credentials_token(config=config, scope="accounts:read", user_id=user_id)

  headers = {
    "Authorization": "Bearer {}".format(token["access_token"])
  }

  res = requests.get("{}/accounts".format(api_url), headers=headers)
  return res.json()

def get_identity_public_key(config):
  identity_server = config["identity_service_url"]
  certs = requests.get("{}/oidc/certs".format(identity_server)).json()
  key = next(filter(lambda k: k["use"] == "sig", certs["keys"]), None)

  return jwk.JWK(**key).export_to_pem(private_key=False, password=None)

def verify_id_token(config, id_token, nonce):
  identity_server = config["identity_service_url"]
  public_key = get_identity_public_key(config)
  decoded = jwt.decode(
    id_token,
    public_key, 
    algorithms="RS256", 
    audience=config["client"]["client_id"]
  )

  assert nonce == decoded["nonce"], "nonce in id_token is not equal to expected value"

def post_pushed_authorisation_url(config, payload):
  client_id = config["client"]["client_id"]
  identity_server = config["identity_service_url"]

  client_assertion = get_client_assertion(config)
  params = {
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": client_assertion,
    **payload
  }

  res = requests.post("{}/oidc/request".format(identity_server), data=params)
  return res.json()