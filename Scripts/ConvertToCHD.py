import os
import time

# Get the directory where the script is launched
script_directory = os.getcwd()

# Iterate through files in the script's directory
for root, dirs, files in os.walk(script_directory):
    for file in files:
        # Check if the file has one of the specified extensions
        if file.lower().endswith(('.cue', '.gdi', '.cdi', '.iso', '.img')):
            input_file = os.path.join(root, file)
            output_file = os.path.splitext(input_file)[0] + ".chd"

            # Check if the output file already exists
            if not os.path.exists(output_file):
                # Execute chdman command
                command = f'chdman createcd -i "{input_file}" -o "{output_file}"'
                os.system(command)
                print(f"Converted {input_file} to {output_file}")
                # Introduce a delay of 20 seconds after conversion
                time.sleep(20)
            else:
                print(f"Skipping {input_file} as {output_file} already exists")

input("Conversion complete. Press Enter to exit.")
