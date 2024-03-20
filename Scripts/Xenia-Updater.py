import os
import requests
import zipfile
from bs4 import BeautifulSoup

# Check if psutil is installed, if not, install it
try:
    import psutil
except ImportError:
    print("psutil library not found. Installing...")
    os.system("pip install psutil")
    import psutil

# Define the URL and file names
release_url = "https://github.com/xenia-project/release-builds-windows/releases/latest"
zip_file_name = "xenia_master.zip"
version_file_name = "version.txt"
executable_name = "xenia.exe"

# Check if xenia.exe is running, if yes, terminate it
for proc in psutil.process_iter():
    if proc.name() == executable_name:
        proc.terminate()

# Make a GET request to the release URL
response = requests.get(release_url)

# Parse HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find the title tag
title_tag = soup.find("title")
if title_tag:
    # Extract version from the title
    title_text = title_tag.text.strip()
    version = title_text.split("Release ")[1].split(" ·")[0]

    # Construct the download URL
    download_url = f"https://github.com/xenia-project/release-builds-windows/releases/download/{version}/xenia_master.zip"

    # Check if the version file exists
    if os.path.exists(version_file_name):
        with open(version_file_name, "r") as f:
            current_version = f.read().strip()
    else:
        current_version = None

    # Check if the current version is different from the latest version
    if current_version != version:
        # Download the zip file
        r = requests.get(download_url)
        with open(zip_file_name, "wb") as code:
            code.write(r.content)
        
        # Extract the contents of the zip file
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall('.')
        
        # Write the new version to version.txt
        with open(version_file_name, "w") as f:
            f.write(version)
        
        print("Updated to version:", version)
        
        # Remove the downloaded zip file
        os.remove(zip_file_name)
        print("Removed the downloaded zip file.")
        
    else:
        print("No update available at this moment.")

else:
    print("Failed to find title tag in the HTML content.")
