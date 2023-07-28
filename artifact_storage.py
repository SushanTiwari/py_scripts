import csv
import random
import string
import requests

#NOTE:
# If you want to perform the scan request on the staging/prod environment,please chase BASE_URL and set VERIFY_CERTIFICATE to True
# If you want to scan locally, update BASE_URL and set VERIFY_CERTIFICATE to FALSE
# then also uncomment the line 98 to manually scan the files locally.

BASE_URL = "http://localhost:5001"
#BASE_URL = "https://artifact-storage.staging.totalexpert.io"
VERIFY_CERTIFICATE = False  # Set to True if you want to verify SSL certificates, False to disable verification

#Iterations and number of rows and columns can be adjusted as per the requirement
NUMBER_OF_ITERATIONS = 10  # Adjust the number of iterations here
CSV_ROWS = 5  # Adjust the number of rows here
CSV_COLUMNS = 5  # Adjust the number of columns here

# Function to generate a random filename
def generate_random_filename():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(10)) + ".csv"

# Function to generate a CSV file with random data and return its filename
def generate_csv_file(file_path, num_rows, num_columns):
    row_headers = [generate_random_string(5) for _ in range(num_rows)]
    column_headers = [f"Column_{i+1}" for i in range(num_columns)]

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the column headers
        writer.writerow([""] + column_headers)

        # Write the rows with random data
        for header in row_headers:
            row_data = [generate_random_string(5) for _ in range(num_columns)]
            writer.writerow([header] + row_data)

    return file_path

# Function to generate a random string
def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

# Function to perform the HTTP POST request and extract "uploadUrl" from JSON response
def perform_post_request(filename):
    url = f"{BASE_URL}/v1/artifact/a?filename={filename}"
    response = requests.post(url, data='', verify=VERIFY_CERTIFICATE)

    if response.status_code == 201:
        json_response = response.json()
        upload_url = json_response.get("uploadUrl")
        artifact_id = json_response.get("artifact", {}).get("artifactId")
        if upload_url:
            # Extract and print the 'artifactId'
            artifact_id = json_response.get("artifact", {}).get("artifactId")
            if artifact_id:
                print(f"Extracted 'artifactId': {artifact_id}")
            else:
                print("No 'artifactId' found in the response.")
            return upload_url,artifact_id
        else:
            print("No 'uploadUrl' found in the response.")
    else:
        print(f"Failed to make the POST request. Status Code: {response.status_code}")

def perform_post_scan_request(artifact_id):
    url = f"http://localhost:5010/v1/scan/{artifact_id}"
    response = requests.post(url,verify=VERIFY_CERTIFICATE)

    if response.status_code == 202:
        print("Scan request successful.")
    else:
        print(f"Failed to perform scan request. Status Code: {response.status_code}")

if __name__ == "__main__":

    for _ in range(NUMBER_OF_ITERATIONS):
        csv_file_path = generate_random_filename()  # Generate a random CSV file path
        csv_file_path = generate_csv_file(csv_file_path, CSV_ROWS, CSV_COLUMNS)  # Create and save the CSV file
        print(f"CSV file with row headers and columns created and saved as '{csv_file_path}'")

        upload_url, artifact_id = perform_post_request(csv_file_path)  # Get the upload URL and artifactId
        if upload_url:
            with open(csv_file_path, 'r') as csv_file:
                csv_content = csv_file.read()

            headers = {'Content-Type': 'text/plain'}
            response = requests.put(upload_url, headers=headers, data=csv_content,verify=VERIFY_CERTIFICATE)

            if response.status_code == 200:
                print(f"CSV file uploaded successfully")
                print(f"Extracted 'artifactId': {artifact_id}")
                #NOTE: Uncomment the below line to perform the scan request locally
                perform_post_scan_request(artifact_id)  # Perform POST request for scan
            else:
                print(f"Failed to upload CSV file. Status Code: {response.status_code}")

        print("-" * 50)
