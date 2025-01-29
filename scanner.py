import csv
import random
import string
import requests
import os

# Define the function
def perform_post_scan_request(artifact_id):
    url = f"https://clamav-scanner.artifact-storage.production.totalexpert.io/v1/scan/{artifact_id}"
    response = requests.post(url, verify=VERIFY_CERTIFICATE)

    if response.status_code == 202:
        print("Scan request successful.")
    else:
        print(f"Failed to perform scan request for artifact ID {artifact_id}. Status Code: {response.status_code}")

# Sample array of artifact IDs
artifact_ids = [
"be9e0464-3524-48d8-a9b6-9460589da110",
    "63ba42a0-83c0-4f06-9b46-d4824134b273",
    "f6f6a5f5-8c79-42e8-8efb-d07d70d58e13",
    "5ad994fb-e18d-4e8b-a0dc-fc195e046176",
    "12826dce-32a5-455b-bc26-bd6b6279186f",
    "850956a2-acf4-40c9-ab6d-45d123680d62",
    "7301326f-2ff2-4d31-9f78-caf3236a1198",
    "447fb5f5-ddf6-49e5-968b-b0cfdf328cf4",
    "e4b9334e-1f22-435d-bfae-0638739e0425"
]


# Assuming VERIFY_CERTIFICATE is defined somewhere in your code
VERIFY_CERTIFICATE = True  # Change it to False if you don't want to verify certificates

# Iterate over each artifact ID and perform scan request
for artifact_id in artifact_ids:
    perform_post_scan_request(artifact_id)
