import os
import requests
from urllib.parse import urljoin

def download_roms(base_urls, rom_list_file, destination_folder):
    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    print(f"The roms will be downloaded in: {destination_folder}")

    # Read the rom list from the file
    with open(rom_list_file, 'r') as file:
        rom_list = [line.strip() for line in file.readlines()]

    # Initialize a list to keep track of missing roms
    missing_roms = []

    # Check if missing_roms_log.txt is not empty, start on a new line
    log_file_path = 'missing_roms_log.txt'
    if os.path.exists(log_file_path) and os.stat(log_file_path).st_size != 0:
        with open(log_file_path, 'a') as log_file:
            log_file.write('\n')

    # Check for missing roms in the destination folder and add them to the log
    present_roms = [f for f in os.listdir(destination_folder) if f.endswith('.zip')]
    new_missing_roms = [rom for rom in rom_list if rom.split(' (')[0] + '.zip' not in present_roms]

    if new_missing_roms:
        with open(log_file_path, 'a') as log_file:
            log_file.write('\n'.join(new_missing_roms))
            log_file.write('\n')

    # Iterate through each rom in the list
    for rom_name in rom_list:
        # Extract the rom filename from the rom_name
        rom_filename = rom_name.split(' (')[0] + '.zip'

        # Flag to check if the rom is found
        rom_found = False

        # Try each base URL
        for base_url in base_urls:
            # Create the download URL
            if "MAME_2010_full_nonmerged_romsets" in base_url:
                download_url = urljoin(base_url, f"roms.zip/roms%2F{rom_filename}")
            else:
                download_url = urljoin(base_url, rom_filename)

            # Check if the rom already exists in the destination folder
            if rom_filename in present_roms:
                print(f"{rom_filename} already exists.")
                rom_found = True
                break  # No need to try the alternative link if the rom is already downloaded
            else:
                # Download the rom
                print(f"Downloading {rom_filename} from {download_url}...")
                response = requests.get(download_url)
                
                # Check if the download was successful (status code 200) and the content is not empty
                if response.status_code == 200 and response.content:
                    with open(os.path.join(destination_folder, rom_filename), 'wb') as rom_file:
                        rom_file.write(response.content)
                    rom_found = True
                    break  # Break the loop if the rom is successfully downloaded
                else:
                    # Add the missing rom to the list
                    missing_roms.append(rom_filename)

        # Update the missing log only if the rom is not found
        if not rom_found:
            with open(log_file_path, 'a') as log_file:
                log_file.write(rom_filename + '\n')

    # Print missing roms
    if missing_roms:
        print("\nMissing roms:")
        for missing_rom in missing_roms:
            print(missing_rom)
        print(f"\nMissing roms logged in '{log_file_path}'")
    else:
        print("\nAll roms are up to date.")

    # Remove entries for successfully downloaded roms from missing_roms_log.txt
    remove_entries_from_log(destination_folder, 'missing_roms_log.txt', missing_roms)

def remove_entries_from_log(destination_folder, log_file_path, successful_downloads):
    # Get the full path of the log file
    log_file_path = os.path.join(destination_folder, log_file_path)

    # Read the existing log file
    with open(log_file_path, 'r') as log_file:
        log_lines = log_file.readlines()

    # Remove entries for successfully downloaded roms
    new_log_lines = [line.strip() for line in log_lines if line.strip() not in successful_downloads]

    # Write the updated log file
    with open(log_file_path, 'w') as log_file:
        log_file.write('\n'.join(new_log_lines))

if __name__ == "__main__":
    base_urls = [
        "https://archive.org/download/MAME0.139RomCollectionByGhostware/",
        "https://archive.org/download/MAME_2010_full_nonmerged_romsets/"
    ]
    rom_list_file = "TimeCapsuleRomList.txt"
    destination_folder = os.path.dirname(os.path.abspath(__file__))

    download_roms(base_urls, rom_list_file, destination_folder)
