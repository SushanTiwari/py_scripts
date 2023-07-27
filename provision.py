import requests
import random
import string

# Function to generate a random filename
def generate_random_filename():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(10)) + ".csv"

# Function to perform the HTTP POST request and extract "uploadUrl" from JSON response
def perform_post_request(filename):
    url = f"http://localhost:5001/v1/artifact/a?filename={filename}"
    response = requests.post(url, data='')

    if response.status_code == 201:
        json_response = response.json()
        upload_url = json_response.get("uploadUrl")
        if upload_url:
            print(f"Response:\n{json_response}")
            print(f"Extracted 'uploadUrl': {upload_url}")
        else:
            print("No 'uploadUrl' found in the response.")
    else:
        print(f"Failed to make the POST request. Status Code: {response.status_code}")

if __name__ == "__main__":
    iterations = int(input("Enter the number of iterations: "))

    for _ in range(iterations):
        filename = generate_random_filename()
        perform_post_request(filename)
        print("-" * 30)
