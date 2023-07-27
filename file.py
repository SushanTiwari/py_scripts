import csv
import random
import string

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def create_csv_file(file_path):
    row_headers = [generate_random_string(5) for _ in range(10)]
    column_headers = [f"Column_{i+1}" for i in range(10)]

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the column headers
        writer.writerow([""] + column_headers)

        # Write the rows with random data
        for header in row_headers:
            row_data = [generate_random_string(5) for _ in range(10)]
            writer.writerow([header] + row_data)

def read_csv_file(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(", ".join(row))

if __name__ == "__main__":
    csv_file_path = 'example.csv'
    create_csv_file(csv_file_path)

    print("CSV file with row headers and columns created and saved as 'example.csv'")
    print("\nCSV File Data:")
    read_csv_file(csv_file_path)
