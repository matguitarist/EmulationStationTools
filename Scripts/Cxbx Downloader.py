import os
import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup

def download_latest_release():
    # GitHub URL for the Cxbx releases
    github_url = 'https://github.com/Cxbx-Reloaded/Cxbx-Reloaded/releases'

    # Send a GET request to the GitHub releases page
    response = requests.get(github_url)
    if response.status_code != 200:
        print(f"Failed to retrieve GitHub page. Status code: {response.status_code}")
        return

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the latest release download link
    latest_release_link = None
    for h2_tag in soup.find_all('h2'):
        if 'CI-' in h2_tag.text:
            latest_release_link = h2_tag.text.strip()
            break

    if not latest_release_link:
        print("Couldn't find a valid download link for the latest release.")
        return

    # Construct the complete download URL for the latest release
    latest_download_url = f'https://github.com/Cxbx-Reloaded/Cxbx-Reloaded/releases/download/{latest_release_link}/CxbxReloaded-Release-VS2022.zip'

    # Get the file name from the URL
    file_name = latest_download_url.split('/')[-1]

    # Check if version.txt exists
    version_file = 'version.txt'
    if os.path.exists(version_file):
        # Read the content of version.txt
        with open(version_file, 'r') as file:
            version_content = file.read().strip()

        # Compare version content with the latest_release_link
        if version_content == latest_release_link:
            print("The files are already at the latest version.")
            return

    else:
        # Create version.txt and write the latest_release_link
        with open(version_file, 'w') as file:
            file.write(latest_release_link)
            print(f"Created version.txt with the latest version: {latest_release_link}")

    # Download the release zip file
    print(f"Downloading {file_name} from {latest_download_url}...")
    file_content = requests.get(latest_download_url).content

    # Save the file in the same directory as the script
    with open(file_name, 'wb') as file:
        file.write(file_content)

    print(f"{file_name} downloaded successfully.")

    # Extract the contents of the zip file to the current directory
    with ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall()

    print(f"{file_name} extracted successfully.")

    # Remove the downloaded zip file
    os.remove(file_name)
    print(f"{file_name} removed.")

if __name__ == "__main__":
    download_latest_release()
    input("Press Enter to exit...")

