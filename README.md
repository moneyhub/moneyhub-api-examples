# Moneyhub API Examples
The purpose of this repo is to show how to communicate with our API in various programming languages to help you get started.

Each directory will map to a programming language which will achieve the following actions:

- Generating an authorisation URL for a AIS connection (while registering a user)
- Generating an authorisation URL for a PIS connection
- Completing a connection by exchanging a code for tokens
- Requesting a client credentials token to access data
- Making a data request to get accounts data

The examples will assume you will be using an API client with full production configuration, which includes:

- Client authentication set to `private_kwy_jwt`
- A JWKS configured
- Request object signing algorithm set to `RS256` 
- `grant_type` set to have:
  - `client_credentials`
  - `authorization_code`
  - `refresh_token`
  - `implicit`
- `response_type` of `code id_token` 

Each directory will have instructions on how to run the examples.