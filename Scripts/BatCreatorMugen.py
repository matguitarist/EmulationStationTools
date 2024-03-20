# This Python script recursively searches for .exe files in subfolders of the main directory,
# creating batch files in the main folder to launch each discovered .exe. 
# Existing batch files are skipped, and the user is informed of the script's actions.
 

import os

def find_exe_and_create_batch(root_folder):
    # Get immediate subfolders (level 1) in the root folder
    subfolders_level1 = [f.path for f in os.scandir(root_folder) if f.is_dir()]

    for first_subfolder in subfolders_level1:
        # Find .exe files in the first subfolder
        exe_files = [os.path.join(first_subfolder, f) for f in os.listdir(first_subfolder) if os.path.isfile(os.path.join(first_subfolder, f)) and f.lower().endswith('.exe')]

        if exe_files:
            chosen_exe_file = exe_files[0]

            # Get the subfolder name
            subfolder_name = os.path.basename(first_subfolder)

            # Rename the chosen_exe_file to match the subfolder name
            new_exe_file_path = os.path.join(os.path.dirname(chosen_exe_file), f'{subfolder_name}.exe')

            # Check if the file with the desired name already exists
            if not os.path.exists(new_exe_file_path):
                os.rename(chosen_exe_file, new_exe_file_path)
                print(f"Renamed '{chosen_exe_file}' to '{new_exe_file_path}'.")

            # Create a batch file in the root folder to launch the renamed .exe file
            batch_file_path = os.path.join(root_folder, f'{subfolder_name}.bat')

            # Check if the batch file already exists
            if not os.path.exists(batch_file_path):
                create_batch_file(new_exe_file_path, batch_file_path)
                print(f"Batch file '{batch_file_path}' created successfully.")
            else:
                print(f"Batch file '{batch_file_path}' already exists. Skipped.")

def create_batch_file(exe_file_path, batch_file_path):
    with open(batch_file_path, 'w') as batch_file:
        batch_file.write(f'@echo off\n')
        batch_file.write(f'cd /d "{os.path.dirname(exe_file_path)}"\n')
        batch_file.write(f'"{exe_file_path}"\n')

if __name__ == "__main__":
    root_folder = os.path.dirname(os.path.abspath(__file__))  # Use the folder where the script is launched
    find_exe_and_create_batch(root_folder)
