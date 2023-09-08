import os
import shutil

def delete_bin_obj_folders(root_directory):
    deleted_folders = []

    for foldername, subfolders, filenames in os.walk(root_directory):
        if 'bin' in subfolders:
            bin_folder_path = os.path.join(foldername, 'bin')
            shutil.rmtree(bin_folder_path)
            deleted_folders.append(bin_folder_path)
        if 'obj' in subfolders:
            obj_folder_path = os.path.join(foldername, 'obj')
            shutil.rmtree(obj_folder_path)
            deleted_folders.append(obj_folder_path)
        if '.build' in subfolders:
            obj_folder_path = os.path.join(foldername, '.build')
            shutil.rmtree(obj_folder_path)
            deleted_folders.append(obj_folder_path)

    return deleted_folders

if __name__ == "__main__":
    folder_directory = input("Enter the folder directory: ")

    if os.path.exists(folder_directory):
        deleted_folders = delete_bin_obj_folders(folder_directory)
        if deleted_folders:
            print("Deleted folders:")
            for folder_path in deleted_folders:
                print(folder_path)
        else:
            print("No 'bin' or 'obj' folders found.")
    else:
        print("Invalid directory path.")
