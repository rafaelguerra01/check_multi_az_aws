#!/usr/bin/python
import os
os.system('clear')

import requests
import subprocess
import json


cmd_ocm_login= "/usr/local/bin/ocm login --token $(cat /tmp/.ocm_token)"
# Execute the command and capture the output
completed_process = subprocess.run(cmd_ocm_login, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Check if the command completed successfully (return code 0)
if completed_process.returncode == 0:
    # Access the output stream
    stdout = completed_process.stdout
    
    # Store the output in a variable
    cmd1_output = stdout.strip()  # Use .strip() to remove leading/trailing whitespaces
    
else:
    print(f"Command failed with return code {completed_process.returncode}")

cmd_ocm_token = "/usr/local/bin/ocm token"
# Execute the command and capture the output
completed_process = subprocess.run(cmd_ocm_token, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Check if the command completed successfully (return code 0)
if completed_process.returncode == 0:
    # Access the output stream
    stdout = completed_process.stdout
    
    # Store the output in a variable
    bearer_token = stdout.strip()  # Use .strip() to remove leading/trailing whitespaces
    
else:
    print(f"Command failed with return code {completed_process.returncode}")

# Replace the URL with the actual endpoint you want to make a GET request to
url = 'https://api.openshift.com/api/clusters_mgmt/v1/cloud_providers/aws/regions'

# Replace 'YOUR_BEARER_TOKEN' with your actual bearer token
# Set the headers with the bearer token
headers = {
    'Authorization': f'Bearer {bearer_token}'
}

# Make the GET request with the headers
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Access the response data
    response_data = json.loads(response.text) 
    print('Total Number of AZs:', len(response_data['items']))
    print ('')
    # Remove unwanted key-value pairs
    unwanted_keys = ['kind', 'page', 'size', 'total']  # List of keys to remove
    for key in unwanted_keys:
      response_data.pop(key, None)  # Remove key if present
    for item in range(len(response_data['items'])):
      print ('Name:', json.dumps(response_data["items"][item]["display_name"]))
      print ('Region:', json.dumps(response_data["items"][item]["id"]))
      print ('Multi_AZ Support:', json.dumps(response_data["items"][item]["supports_multi_az"]))
      print ('#############################################')
else:
    print(f'Request failed with status code {response.status_code}')

