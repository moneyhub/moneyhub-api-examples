# Moneyhub API Examples - Python
To use the Moneyhub API in Python. Due to there not being a great library that handles all the high security features of OIDC, including: request objects, private key JWT token end point authorisation; a lot of the OIDC features are written manually, which could help you to write your own in different languages if the client libraries aren't there.

These examples should work in either python 2 or 3.

## Prerequisites
- Run `pip -r requirements.txt` inside this directory
- Run the commands below for each script

## Get AIS Authorisation URL
```shell
python src/get_ais_auth_url.py
```

## Get PIS Authorisation URL
```shell
python src/get_pis_auth_url_with_created_payee.py
```

OR 
```shell
python src/get_pis_auth_url_without_created-payee.py
```

Both of these scripts produce the same result, but differ in how the payee is managed

## Exchange Code for Tokens
```shell
python src/exchange_code_for_tokens.py -c <AUTH_CODE> -i <ID_TOKEN>
```

## Get Accounts
Take the `sub` value from the `id_token` returned above
```shell
python src/get_accounts.py -u <USER_ID>
```