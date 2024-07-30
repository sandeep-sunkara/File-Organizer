import os
import shutil
import logging
from datetime import datetime

# Setting logging
logging.basicConfig(filename='file_organizer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_last_modified_time(path):  # Returns modified date and time
    timestamp = os.path.getmtime(path)
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def organize_files(path):
    try:
        files = os.listdir(path)  # List of files in directory

        for file in files:
            full_path = os.path.join(path, file)  # Takes the path including extension

            if os.path.isfile(full_path):
                filename, extension = os.path.splitext(file)  # Separates name and extension
                extension = extension[1:]

                if extension:
                    dest_dir = os.path.join(path, extension)
                    if not os.path.exists(dest_dir):  # Create directory if it doesn't exist
                        os.makedirs(dest_dir)
                        logging.info(f"Created directory: {dest_dir}")
                    shutil.move(full_path, os.path.join(dest_dir, file))
                    logging.info(f"Moved file: {full_path} to {dest_dir}")
                else:
                    logging.warning(f"File without extension found: {full_path}")
    except Exception as e:
        logging.error(f"Error organizing files: {e}")

def delete_empty_dirs(path):
    try:
        empty_dirs = [dirpath for dirpath, dirnames, filenames in os.walk(path, topdown=False) if not dirnames and not filenames]
        if not empty_dirs:  # Check if there are no empty directories
            print("No empty directories found.")
            logging.info("No empty directories found.")
        else:
            for dirpath in empty_dirs:
                os.rmdir(dirpath)
                print(f"Deleted empty directory: {dirpath}")
                logging.info(f"Deleted empty directory: {dirpath}")
    except Exception as e:
        print(f"Error deleting empty directories: {e}")
        logging.error(f"Error deleting empty directories: {e}")

if __name__ == "__main__":
    while True:
        path = input('Enter Path: ')  # Takes input of directory path
        if os.path.exists(path) and os.path.isdir(path):
            last_modified = get_last_modified_time(path)
            print(f"Last modified time before organizing: {last_modified}")  # Shows the last modified time
            logging.info(f"Last modified time before organizing: {last_modified}")

            organize_files(path)  # Calls the path organizer

            last_modified_after = get_last_modified_time(path)
            print(f"Last modified time after organizing: {last_modified_after}")
            logging.info(f"Last modified time after organizing: {last_modified_after}")

            delete_empty = input("Do you want to delete empty directories after organizing files? (yes/no): ").strip().lower()

            if delete_empty == "yes":
                delete_empty_dirs(path)
                last_modified_after_deletion = get_last_modified_time(path)
                print(f"Last modified time after deleting empty directories: {last_modified_after_deletion}")
                logging.info(f"Last modified time after deleting empty directories: {last_modified_after_deletion}")
                break
            elif delete_empty == "no":
                break
            else:
                logging.error("Invalid input provided. Please enter 'yes' or 'no'.")
        else:
            print("Invalid path provided. Please provide a valid directory path.")
            logging.error("Invalid path provided. Please provide a valid directory path.")
            print()
