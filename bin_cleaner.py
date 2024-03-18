import os

def clear_folder(folder_path):
    # Iterate over all files and subdirectories in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        # Check if the item is a file
        if os.path.isfile(item_path):
            # Remove the file
            os.remove(item_path)
        # Check if the item is a directory
        elif os.path.isdir(item_path):
            # Remove the directory and its contents recursively
            clear_folder(item_path)
            os.rmdir(item_path)