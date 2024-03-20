import os
import requests
from zipfile import ZipFile
import shutil
import subprocess

def install_missing_libraries():
    try:
        import requests
        from bs4 import BeautifulSoup
        import shutil
    except ImportError as e:
        print(f"Installing missing library: {e.name}")
        subprocess.call(['pip', 'install', e.name])

def download_latest_release():
    # Install missing libraries
    install_missing_libraries()

    from bs4 import BeautifulSoup  # Import BeautifulSoup after installation

    # GitHub URL for the Citra nightly releases
    github_url = 'https://github.com/citra-emu/citra-nightly/releases'

    # Send a GET request to the GitHub releases page
    response = requests.get(github_url)
    if response.status_code != 200:
        print(f"Failed to retrieve GitHub page. Status code: {response.status_code}")
        return

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the latest release download link
    latest_release_link = None
    for a_tag in soup.find_all('a', {'href': lambda x: x and x.endswith('.zip')}):
        if 'citra-windows-msvc-' in a_tag['href']:
            latest_release_link = a_tag['href']
            break

    if not latest_release_link:
        print("Couldn't find a valid download link for the latest release.")
        return

    # Extracting version from the latest release link
    latest_release_version = latest_release_link.split('/')[-2]  # Extracting the part before .zip

    # Construct the complete download URL for the latest release
    latest_download_url = f'https://github.com{latest_release_link}'

    # Get the file name from the URL
    file_name = f'citra-windows-msvc-{latest_release_version}.zip'

    # Check if version.txt exists
    version_file = 'version_citra.txt'
    if os.path.exists(version_file):
        # Read the content of version.txt
        with open(version_file, 'r') as file:
            version_content = file.read().strip()

        # Compare version content with the latest_release_version
        if version_content == latest_release_version:
            print("The files are already at the latest version.")
            return

    else:
        # Create version.txt and write the latest_release_version
        with open(version_file, 'w') as file:
            file.write(latest_release_version)
            print(f"Created version_citra.txt with the latest version: {latest_release_version}")

    # Download the release zip file
    print(f"Downloading {file_name} from {latest_download_url}...")
    file_content = requests.get(latest_download_url).content

    # Save the file in the same directory as the script
    with open(file_name, 'wb') as file:
        file.write(file_content)

    print(f"{file_name} downloaded successfully.")

    # Extract the contents of the zip file to a temporary folder
    extract_folder = f'citra-windows-msvc-{latest_release_version}'
    with ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    print(f"{file_name} extracted successfully.")

    # Move the contents of the extracted folder to the root folder
    for item in os.listdir(extract_folder):
        src = os.path.join(extract_folder, item)
        dst = os.path.join(os.getcwd(), item)
        if os.path.isdir(src):
            # If it's a directory, move its contents
            for sub_item in os.listdir(src):
                sub_src = os.path.join(src, sub_item)
                sub_dst = os.path.join(os.getcwd(), sub_item)
                if os.path.exists(sub_dst):
                    if os.path.isdir(sub_dst):
                        shutil.rmtree(sub_dst)
                    else:
                        os.remove(sub_dst)
                shutil.move(sub_src, sub_dst)
            # Remove the empty directory after moving its contents
            os.rmdir(src)
        else:
            # If it's a file, simply move it
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            shutil.move(src, dst)

    print("Contents moved to the root folder.")

    # Remove the temporary extract folder
    shutil.rmtree(extract_folder)
    print("Temporary extract folder removed.")

    # Remove the downloaded zip file
    os.remove(file_name)
    print(f"{file_name} removed.")

if __name__ == "__main__":
    download_latest_release()
    input("Press Enter to exit...")
