# This script synchronizes files between a source and a replica folder.
# Usage instructions can be found in the README file in the GitHub repository.

import os
import shutil
import hashlib
import time
import argparse
import logging

# Set up logging
def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file, 
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s")

def log_message(message):
    print(message)
    logging.info(message)    

# Function to check if the source and replica folders exist
def check_folders(source_folder, replica_folder):
    if not os.path.exists(source_folder):
        log_message(f"Error: Source folder {source_folder} does not exist.")
        return False
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)
        log_message(f"Replica folder {replica_folder} created.")
    return True    

# Function to get MD5 hash of a file
def get_md5(file_path):
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except Exception as e:
        log_message(f"Error computing MD5 for file {file_path}: {e}")
        return None
    return hash_md5.hexdigest()

# Function to synchronize files between two folders
def sync_folders(source_folder, replica_folder, delete=False):
    
    # Get a list of all files and folders in the source folder
    for root, folders, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            replica_path = os.path.join(replica_folder, os.path.relpath(source_path, source_folder))

            # Check if the path is a folder and create it in the replica folder
            if not os.path.exists(replica_path) or get_md5(source_path) != get_md5(replica_path):
                log_message(f"Copying: {source_path} to {replica_path}")
                try:
                    shutil.copy2(source_path, replica_path)
                except Exception as e:
                    log_message(f"Error copying file {source_path} to {replica_path}: {e}")

        for folder in folders:
            source_path = os.path.join(root, folder)
            replica_path = os.path.join(replica_folder, os.path.relpath(source_path, source_folder))

            # Check if the path is a folder and create it in the replica folder
            if not os.path.exists(replica_path):
                os.makedirs(replica_path)

    # Clean up files in the replica folder that are not in the source folder, if delete flag is set
    if delete:
        for root, folders, files in os.walk(replica_folder):
            for folder in folders:
                replica_path = os.path.join(root, folder)
                source_path = os.path.join(source_folder, os.path.relpath(replica_path, replica_folder))

                # Check if the file exists in the source folder
                if not os.path.exists(source_path):
                    log_message(f"Deleting: {replica_path}")
                    try:
                        shutil.rmtree(replica_path)
                    except Exception as e:
                        log_message(f"Error deleting folder {replica_path}: {e}")

            for file in files:
                replica_path = os.path.join(root, file)
                source_path = os.path.join(source_folder, os.path.relpath(replica_path, replica_folder))

                # Check if the file exists in the source folder
                if not os.path.exists(source_path):
                    log_message(f"Deleting: {replica_path}")
                    try:
                        os.remove(replica_path)
                    except Exception as e:
                        log_message(f"Error deleting file {replica_path}: {e}")

# Main function to parse command-line arguments and synchronize folders
def main():
    parser = argparse.ArgumentParser(description="Synchronize source and replica folders.")

    # Parse command-line arguments
    parser.add_argument("source_folder", help="The source folder to synchronize from.")
    parser.add_argument("replica_folder", help="The replica folder to synchronize to.")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete files in replica that are not in source.")
    parser.add_argument("-i", "--interval", type=int, default=60, help="Time interval (in seconds) between synchronizations.")
    parser.add_argument("-l", "--log", help="Path to the log file", required=True)
    
    # Parsing arguments
    args = parser.parse_args()

    # Initialize logging
    setup_logging(args.log)

    # If the delete flag is set, print a warning message
    if args.delete:
        log_message("Warning: Files in the replica folder that are not in the source folder will be deleted.")
    
    # Check the source and replica folders
    if not check_folders(args.source_folder, args.replica_folder):
        return

    # Synchronize the folders
    while True:
        log_message(f"\nSynchronizing folders {args.source_folder} to {args.replica_folder}...")
        sync_folders(args.source_folder, args.replica_folder, delete=args.delete)
        log_message(f"\nSynchronization complete. Waiting for {args.interval} seconds before next sync.")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
