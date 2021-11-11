'''
This piece finds the flow ID
        req = requests.get(
            f'https://tableau.website.org/api/3.11/sites/siteid/flows?filter=name:eq:{flowname}',
            headers=headers
        )
This piece finds if it ran
        req = requests.get(
            f'https://tableau.website.org/api/3.11/sites/siteid/flows/runs?filter=flowId:eq:{flowID}&sort=completedAt:desc',
            headers=headers
        )
This piece runs the flow
        s.post(
            f'https://tableau.website.org/api/3.11/sites/siteid/flows/{flowID}/run',
            json=payload
        )
'''


import os
import sys
import time
import pandas as pd
import datetime
from datetime import date
from datetime import timedelta
import json
from io import StringIO
import json
import requests

today = datetime.date.today()
yesterday = today - timedelta(days=1)
timestr = time.strftime("%Y%m%d-%H%M%S")

print('Starting Session')

s = requests.Session()
print('Session Started')

print('Obtaining List of Flows to Run...')
flowlist = ['Flow Name']
print(f'...the flows to run are {flowlist}')


# Login/logout code taken from https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_auth.htm
# NOTE! Substitute your own values for the following variables

# True = use personal access token for sign in, false = use username and password for sign in.
use_pat_flag = False
print('Using UN/PW to log in to Tableau...')
# print(datetime.datetime.now(), "Using UN/PW to sign in to Tableau...")

print('... setting server name, version, and site url id...')

# Name or IP address of your installation of Tableau Server
server_name = "tableau.website.org"
print(f'the server name is {server_name}')
version = "3.11"  # API version of your server
print(f'the version is {version}')
# Site (subpath) to sign in to. An empty string is used to specify the default site.
site_url_id = ""
print(f'the site uri id is {site_url_id}')

# For username and password sign in
print('...setting username and password (admin)...')

user_name = "username"  # input # User name to sign in as (e.g. admin)
password = "password"  # {password}
# For Personal Access Token sign in
# Name of the personal access token.
# !NOTE Need to change based on active user accounts and tokens. Make sure the token is active, if not then tasks WILL fail
print('...setting PAT and PAT secret...')

personal_access_token_name = "test"
# Value of the token.
personal_access_token_secret = "secret:string"
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


print('Running and checking flow')

def runandcheckflow():
    flowidlist = []
    for flowname in flowlist:
        # Find the flow id
        print(f'Finding FlowID for {flowname}')
        # find flow id
        req = requests.get(
            f'https://tableau.website.org/api/3.11/sites/siteid/flows?filter=name:eq:{flowname}',
            headers=headers
        )
        print('request sent')
        response = json.dumps(json.loads(req.content), sort_keys=True, indent=4)

        item_dict = json.loads(response)
        item_str = str(item_dict)
        item_str = item_str.split()
        print(f'the response is: {item_str}')
        mylist = []
        for item in item_str:
            mylist.append(item)

        flowID = mylist[9]
        flowID = flowID.replace("'", '')
        flowID = flowID.replace(',', '')
        print(f'The flowID is {flowID}')

        flowidlist.append(flowID)

    for flowID in flowidlist:
        # Get today's date
        todaysdate = today
        print(f'Today is {todaysdate}')
        print(f'Finding if flow {flowID} ran for {todaysdate}')
        req = requests.get(
            f'https://tableau.website.org/api/3.11/sites/siteid/flows/runs?filter=flowId:eq:{flowID}&sort=completedAt:desc',
            headers=headers
        )
        print('request sent')
        response = json.dumps(json.loads(req.content), sort_keys=True, indent=4)
        item_dict = json.loads(response)
        item_str = str(item_dict)
        item_str = item_str.split()
        print('request gathered')
        mylist = []
        for item in item_str:
            mylist.append(item)
        print('checking to see if run')
        lastrun = mylist[0:20]
        status = mylist[0:20]
        lastrun = str(lastrun)
        status = str(status)
        todaysdate = str(todaysdate)

        if todaysdate in lastrun:
            print(f'The flow {flowID} kicked off for {todaysdate}')

            if "Success" in status:
                print(f'The flow {flowID} Succeded for {todaysdate}. No need to rerun.')

            elif "InProgress" in status:
                print(f'The flow {flowID} is in progress for {todaysdate} waiting 5 minutes before retrying')


            elif "Pending" in status:
                print(f'The flow {flowID} is pending for {todaysdate} waiting 5 minutes before retrying')


            elif 'Failed' in status:  # if flow did not run, then run the flow
                print(f'The flow {flowID} did not run successfully for {todaysdate}. Running flow {flowID}')
                # s.post(
                #     f'https://tableau.website.org/api/3.11/sites/siteid/flows/{flowID}/run',
                #     json=payload
                # )
                # time.sleep(1200)


            else:
                print('unknown error, good luck charlie')
        elif todaysdate not in lastrun:
            print(f'The flow {flowID} has not run for today, running now')
            # s.post(
            #     f'https://tableau.website.org/api/3.11/sites/siteid/flows/{flowID}/run',
            #     json=payload
            # )
            # time.sleep(1200)

        else:
            print('unknown error, good luck charlie')
runandcheckflow()

