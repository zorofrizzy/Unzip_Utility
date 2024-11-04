"""
Python script to unzip both .zip and .gz files in a recursive manner.
Uses os.walk, zipfile, and gzip modules.
Creates a new subdirectory in the intended root folder. 
All unzipped files will be stored there.
Does not delete original unzipped files by default.

Usage: 
    1. Pass the base directory as a command-line argument:
       Ex: python unzipper.py /home/my/path/here
       Optionally, add `--delete` to delete source files after unzipping:
       Ex: python unzipper.py /home/my/path/here --delete
    2. Call the main function and pass the directory as an argument:
       Ex:
           from unzipper import main
           main('/my/root/directory/here', DELETE_SOURCE_FILES=True)

Returns : Nothing
"""

import zipfile
import gzip
import shutil
import os
import sys

def parse_root_directory(root, DELETE_SOURCE_FILES=False):
    """
    Parse root and create a new directory to store all extracted files.
    Unzips both .zip and .gz files. Deletes original files based on flag.
    """
    print("Root directory:", root)
    base_folder_name = os.path.basename(root) + '_unzip'
    final_destination = os.path.join(root, base_folder_name)

    # Ensure unique folder name
    name_counter = 1
    while os.path.exists(final_destination):
        final_destination = os.path.join(root, f"{base_folder_name}_{name_counter}")
        name_counter += 1

    # Create the final destination directory
    try:
        os.mkdir(final_destination)
    except Exception as e:
        print("Exception occurred while creating the folder:", e)
        return

    # Recursively walk through directories
    for dirpath, _, filenames in os.walk(root):
        for each_file in filenames:
            file_path = os.path.join(dirpath, each_file)

            # Flags to check for successful extraction
            gzip_success = False
            zip_success = False

            # Handle .zip files
            if each_file.endswith('.zip'):
                print("Unzipping .zip file:", file_path)
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(final_destination)
                    print("Unzipped:", each_file)
                    zip_success = True
                except zipfile.BadZipFile:
                    print("Bad zip file:", each_file)

            # Handle .gz files
            elif each_file.endswith('.gz'):
                print("Unzipping .gz file:", file_path)
                try:
                    with gzip.open(file_path, 'rb') as gz_file:
                        output_file_path = os.path.join(final_destination, each_file[:-3])  # Remove .gz extension
                        with open(output_file_path, 'wb') as out_file:
                            shutil.copyfileobj(gz_file, out_file)
                    print("Unzipped:", each_file)
                    gzip_success = True
                except gzip.BadGzipFile:
                    print("Bad gzip file:", each_file)
            
            # Delete files if extraction was successful and deletion flag is set
            if DELETE_SOURCE_FILES and (gzip_success or zip_success):
                os.remove(file_path)
                print("Deleted source file:", file_path)

def main(root='', DELETE_SOURCE_FILES=False):
    if not root:
        raise ValueError("Pass an input directory.")
    if not os.path.isdir(root):
        raise NotADirectoryError(f"Provided path '{root}' is not a directory.")
    parse_root_directory(root, DELETE_SOURCE_FILES)

if __name__ == "__main__":
    root = ''
    DELETE_SOURCE_FILES = '--delete' in sys.argv
    
    if len(sys.argv) > 1:
        root = sys.argv[1] if sys.argv[1] != '--delete' else ''
    
    main(root, DELETE_SOURCE_FILES)
