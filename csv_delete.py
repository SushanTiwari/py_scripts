import os

def delete_csv_files(directory):
    try:
        # Get a list of all files in the directory
        files = os.listdir(directory)
        for file in files:
            # Check if the file has a .csv extension
            if file.endswith('.csv'):
                file_path = os.path.join(directory, file)
                # Delete the file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        print("Deletion of .csv files completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'directory_path' with the path of the directory containing the .csv files
    directory_path = "/Users/sushan.tiwari/Desktop/Code_Repo/py_scripts"
    delete_csv_files(directory_path)
