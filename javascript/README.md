# Moneyhub API Examples - JavaScript
To use the Moneyhub API in JavaScript, the recommended approach is to use our library `@mft/moneyhub-api-client`. All the scripts in this directory make use of the library.

It is recommended to use at least Node v16 to run the scripts. 

## Prerequisites
- Ensure you have Node v16 installed on your machine
- Run `npm i` inside this directory
- Run the commands below for each script

## Get AIS Authorisation URL
```shell
node src/get-ais-auth-url.js
```

## Get PIS Authorisation URL
```shell
node src/get-pis-auth-url-with-created-payee.js
```

OR 
```shell
node src/get-pis-auth-url-without-created-payee.js
```

Both of these scripts produce the same result, but differ in how the payee is managed

## Exchange Code for Tokens
```shell
node src/exchange-code-for-tokens -c <AUTH_CODE>
```

## Get Accounts
Take the `sub` value from the `id_token` returned above
```shell
node src/get-accounts.js -u <USER_ID>
```