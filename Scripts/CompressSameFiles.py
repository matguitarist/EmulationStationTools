import os
from zipfile import ZipFile

def compress_files(input_directory, output_directory):
    # Create a dictionary to store files based on their base names
    file_dict = {}

    # Iterate through files in the input directory
    for filename in os.listdir(input_directory):
        filepath = os.path.join(input_directory, filename)

        # Check if the path is a file
        if os.path.isfile(filepath):
            # Extract the base name without the extension
            base_name, extension = os.path.splitext(filename)

            # If base name is already in the dictionary, append the file path
            if base_name in file_dict:
                file_dict[base_name].append(filepath)
            else:
                # Otherwise, create a new entry in the dictionary
                file_dict[base_name] = [filepath]

    # Iterate through the dictionary and create archives
    for base_name, file_paths in file_dict.items():
        # Construct the output archive path
        archive_path = os.path.join(output_directory, f"{base_name}.zip")

        # Create a new zip archive
        with ZipFile(archive_path, 'w') as zipf:
            # Add each file to the archive
            for file_path in file_paths:
                zipf.write(file_path, os.path.basename(file_path))

        print(f"Archive '{archive_path}' created successfully.")

if __name__ == "__main__":
    # Use the current working directory as the input directory
    input_directory = os.getcwd()

    # Specify the output directory as "output" in the root folder
    output_directory = os.path.join(os.getcwd(), "output")

    # Ensure the output directory exists, if not, create it
    os.makedirs(output_directory, exist_ok=True)

    # Call the function to compress files
    compress_files(input_directory, output_directory)
