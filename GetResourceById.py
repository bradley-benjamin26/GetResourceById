#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import requests
import time
import pandas as pd
import json

aspace_url = 'https://archives-api.lib.umd.edu'
username = input('Username: ')
password = input('Password: ')
file_name = input('Please input a file name: ')
resource_id = input('ID for resource')

#authentication
login_url =f"{aspace_url}/users/{username}/login?password={password}"
#gets session id to enable use of API
response = requests.post(login_url)
auth=response.json()
session = auth["session"]
#session ID is set to a variable for use as a header for the API call
headers = {'X-ArchivesSpace-Session':session}

#checks to see if connection was sucessful or reports any error
if response.status_code==200:
    try:
        #id = ''
       # repo_id = '2'
        #resolve = ''
        query = requests.get(f'{aspace_url}/repositories/2/resources/{resource_id}/ordered_records', headers=headers)
        data =json.loads(query.text)
        #normalizes JSON data. Moves parsing to the record level and skips the uris parent element in the JSON response
        result=pd.json_normalize(data,record_path='uris')
        print(result)
        #writes dataframe to file
        result.to_csv(file_name, index=False)
        exit(1)
    except ValueError:
       print(response.text)
       exit(1)
       print('value error section')
    else:
       print('Error'+''+response.text)
       exit(1)