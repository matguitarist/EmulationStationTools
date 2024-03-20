import os
import shutil

def create_empty_file_and_move(folder_path):
    # Generate the file name based on the folder name
    file_name = os.path.basename(folder_path) + ".scummvm"
    
    # Construct the full file path within the folder
    file_path = os.path.join(folder_path, file_name)

    # Create an empty file with the generated file name
    with open(file_path, 'w'):
        pass

    print(f"Created {file_name} in {folder_path}")

def create_empty_files_and_move_in_directory(directory_path):
    # Iterate through the contents of the specified directory
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)

        # Check if the item is a directory
        if os.path.isdir(folder_path):
            # Call the function to create an empty file in the directory
            create_empty_file_and_move(folder_path)

# Use the current working directory as the base directory
directory_path = os.getcwd()

# Call the function to create empty files in each subdirectory
create_empty_files_and_move_in_directory(directory_path)
