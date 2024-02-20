import requests
import sys
import json
import time
from requests.exceptions import Timeout

# Set the URL for the package update API endpoint
api_url = "REPLACE WITH URL/api/package"

# Set the API key for authentication
api_key = "REPALCE WITH API KEY"

# Set the headers with the API key for authentication
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
"""
# Make a GET request to retrieve the list of available packages
response = requests.get(api_url, headers=headers)

# Check the response
if response.status_code == 200:
    try:
        # Attempt to extract the list of package dictionaries from the response
        available_packages = response.json()
        
        if isinstance(available_packages, list):
            print("List of Available Packages starting with 'docassemble' that can be updated:")
            for package_info in available_packages:
                if (
                   isinstance(package_info, dict) and
                    package_info.get("name", "").startswith("docassemble") and
                    package_info.get("can_update", True)
                ):
                    print(package_info)
        else:
            print("Unexpected response format. Expected a list.")
    except ValueError:
        print("Error decoding JSON response.")
else:
    print(f"Error retrieving package list. Status code: {response.status_code}")
    print("Error Message:", response.text)"""




# Set the base URL for the API and the specific endpoint
base_url = "SAME AS THE API_URL WITHOUT THE /api/package"


def check_update_status(task_id):
    status_endpoint = "/api/package_update_status"
    status_url = f"{base_url}{status_endpoint}"
    params = {"task_id": task_id}

    while True:
        try:
            response = requests.get(status_url, headers=headers, params=params, timeout=7)
            if response.status_code == 200:
                status_info = response.json()
                if status_info.get('status') == 'completed':
                    if status_info.get('ok', False):
                        print("Package update completed successfully.")
                    else:
                        print("Package update failed.", "Error Message:", status_info.get('error_message', 'No error message provided.'))
                    break  
                elif status_info.get('status') == 'working':
                    print("Package update is still in progress.")
                elif status_info.get('status') == 'unknown':
                    print("The task_id has expired or is invalid.")
                    break
                time.sleep(2)  # Wait before checking again
            else:
                print("Failed to retrieve update status. Status code:", response.status_code, "Error Message:", response.text)
                break
        except Timeout:
            print("Request timed out. Trying again...")



update_payload = {'update': 'NAME OF PACKAGE'}  #Use the commented out code to see the names of the packages

# Making the POST request to initiate the package installation/update
response = requests.post(f"{base_url}/api/package", headers=headers, json=update_payload)

# Check if the request was successful
if response.status_code == 200:
    info = response.json()
    task_id = info.get('task_id')
    if task_id:
        print("Update initiated. Task ID:", task_id)
        check_update_status(task_id)  # checking the status
    else:
        print("No task_id found in the response.")
else:
    print("Failed to initiate package update. Status code:", response.status_code, "Error Message:", response.text)

