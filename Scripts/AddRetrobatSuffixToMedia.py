# The script is a Tkinter-based GUI application that renames and organizes files in a specified folder based on subfolder names.
# It adds predefined suffixes to filenames according to the subfolder's purpose,
# moves the renamed files to designated target folders, and provides a log of the executed operations.
# The application is responsive to window resizing.


import os
import shutil

def add_suffix_to_files(folder_path, suffix, target_folder):
    # Iterate through files in the specified folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            # Split the filename and extension
            name, extension = os.path.splitext(filename)

            # Check if the filename already contains the suffix
            if not name.endswith(suffix[1:]):  # Exclude the '-' from the suffix
                # Check the parent folder name and add the appropriate suffix
                new_name = f"{name}{suffix}{extension}"

                # Create the new path and rename the file
                new_path = os.path.join(folder_path, new_name)
                os.rename(file_path, new_path)

                # Move the file to the target folder
                target_path = os.path.join(os.getcwd(), target_folder)
                os.makedirs(target_path, exist_ok=True)
                shutil.move(new_path, os.path.join(target_path, new_name))
            else:
                print(f"Skipping {filename} in {folder_path} as it already has the suffix {suffix}")

def remove_empty_folders(base_folder):
    for root, dirs, files in os.walk(base_folder, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                os.rmdir(dir_path)
                print(f"Removed empty folder: {dir_path}")
            except OSError:
                print(f"Folder not empty: {dir_path}")

if __name__ == "__main__":
    folder_path = os.getcwd()  # Use the current working directory as the base folder

    # Add the desired suffix based on folder name
    folders_to_suffix = {
        "artwork_3d": ("-boxart", "images"),
        "artwork_front": ("-thumb", "images"),
        "fanart": ("-fanart", "images"),
        "logo": ("-marquee", "images"),
        "medium_front": ("-cartridge", "images"),
        "medium_disc": ("-cartridge", "images"),
        "screenshot": ("-image", "images"),       
        "video": ("-videos", "videos")
    }

    for folder_name, (suffix, target_folder) in folders_to_suffix.items():
        folder_path_with_suffix = os.path.join(folder_path, folder_name)
        if os.path.exists(folder_path_with_suffix):
            add_suffix_to_files(folder_path_with_suffix, suffix, target_folder)
        else:
            print(f"Skipping folder: {folder_name} as it doesn't exist.")

    # Remove empty folders
    remove_empty_folders(folder_path)

    input("Press any key to close the script")
