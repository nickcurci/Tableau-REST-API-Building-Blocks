import requests
import json
s = requests.Session()

# Login/logout code taken from https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_auth.htm
# NOTE! Substitute your own values for the following variables

# True = use personal access token for sign in, false = use username and password for sign in.
use_pat_flag = False
print('Using UN/PW to log in to Tableau...')
# print(datetime.datetime.now(), "Using UN/PW to sign in to Tableau...")

print('... setting server name, version, and site url id...')

# Name or IP address of your installation of Tableau Server
server_name = "tableau.steward.org"
print(f'the server name is {server_name}')
version = "3.11"  # API version of your server
print(f'the version is {version}')
# Site (subpath) to sign in to. An empty string is used to specify the default site.
site_url_id = ""
print(f'the site uri id is {site_url_id}')

# For username and password sign in
print('...setting username and password (admin)...')

#UN/PW can be stored in text file

# with open(TU, 'r', encoding='utf-8') as f:
#     user_name = f.read().replace('\n', '')
# with open(TP, 'r', encoding='utf-8') as f:
#     password = f.read().replace('\n', '')

user_name = "username"  # input # User name to sign in as (e.g. admin)
password = "password"  # {password}

# For Personal Access Token sign in
# Name of the personal access token.
# !NOTE Need to change based on active user accounts and tokens. Make sure the token is active, if not then tasks WILL fail
print('...setting PAT and PAT secret...')

# with open(PATN, 'r', encoding='utf-8') as f:
#     personal_access_token_name = f.read().replace('\n', '')
personal_access_token_name = "string"
# # Value of the token.
# with open(PATS, 'r', encoding='utf-8') as f:
#     personal_access_token_secret = f.read().replace('\n', '')
personal_access_token_secret = "long:string"
print('...signing in.')

signin_url = "https://{server}/api/{version}/auth/signin".format(
    server=server_name, version=version)

if use_pat_flag:
    print('using PAT to sign in')
    # The following code constructs the body for the request.
    # The resulting element will look similar to the following example:
    #
    # {
    #   "credentials": {
    #      "personalAccessTokenName": "TOKEN_NAME",
    #      "personalAccessTokenSecret": "TOKEN_VALUE",
    #       "site": {
    #        "contentUrl": ""
    #       }
    #     }
    # }
    #

    payload = {"credentials": {"personalAccessTokenName": personal_access_token_name,
                               "personalAccessTokenSecret": personal_access_token_secret,
                               "site": {"contentUrl": site_url_id}}}

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

else:
    print('signing in')
    # The following code constructs the body for the request. The resulting element will look similar to the following example:
    #
    #
    # {
    #   "credentials": {
    #      "name": "USERNAME",
    #      "password": "PASSWORD",
    #       "site": {
    #        "contentUrl": ""
    #       }
    #     }
    # }
    #

    payload = {"credentials": {"name": user_name,
                               "password": password, "site": {"contentUrl": site_url_id}}}

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

# Send the request to the server
print('sending the request to the server')
req = s.post(signin_url, json=payload, headers=headers)
req.raise_for_status()

# Get the response
response = json.loads(req.content)
print('the response from the server has been recieved')
# Parse the response JSON. The response body will look similar
# to the following example:
#
# {
#   "credentials": {
#      "site": {
#         "id": "xxxxxxxxxx-xxxx-xxxx-xxxxxxxxxx",
#         "contentUrl": ""
#      },
#      "user": {
#         "id": "xxxxxxxxxx-xxxx-xxxx-xxxxxxxxxx"
#      },
#       "token": "CREDENTIALS_TOKEN"
#   }
# }
#

# Get the authentication token from the credentials element
token = response["credentials"]["token"]
print('the token has been recieved')

# Get the site ID from the <site> element
site_id = response["credentials"]["site"]["id"]
print('the site id has been recieved')

print('...Sign In Successful')
print(f'Token: {token}')
print(f'Site ID: {site_id}')

# Set the authentication header using the token returned by the Sign In method.
print('setting headers = token')
headers['X-tableau-auth'] = token
s.headers.update(headers)
print('headings have ben updated')

def timeout_login():
    print('using the timeout login')
    if use_pat_flag:

        payload = {"credentials": {"personalAccessTokenName": personal_access_token_name,
                                   "personalAccessTokenSecret": personal_access_token_secret,
                                   "site": {"contentUrl": site_url_id}}}


    else:

        payload = {"credentials": {"name": user_name,
                                   "password": password, "site": {"contentUrl": site_url_id}}}

    # Send the request to the server
    req = s.post(signin_url, json=payload, headers=headers)
    req.raise_for_status()

    # Get the response
    response = json.loads(req.content)

    # Get the authentication token from the credentials element
    token = response["credentials"]["token"]

    # Get the site ID from the <site> element
    site_id = response["credentials"]["site"]["id"]

    print('...Sign In Successful')
    print(f'Token: {token}')
    print(f'Site ID: {site_id}')

    # Set the authentication header using the token returned by the Sign In method.
    headers['X-tableau-auth'] = token
    s.headers.update(headers)
    print('timeout login was a success')

timeout_login()





