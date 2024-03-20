import os
import shutil
from collections import defaultdict
import re

def move_files_and_create_m3u(root_folder):
    multi_disc_folder = os.path.join(root_folder, "MultiDisc")
    log_file = os.path.join(root_folder, "log.txt")

    # Create MultiDisc folder if it doesn't exist
    if not os.path.exists(multi_disc_folder):
        os.makedirs(multi_disc_folder)

    # Move existing M3U files from MultiDisc to root folder
    for root, _, files in os.walk(multi_disc_folder):
        for file in files:
            if file.endswith(".m3u"):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(root_folder, file)
                shutil.move(source_path, destination_path)

    # Group files by their common names
    disc_groups = defaultdict(list)
    for filename in os.listdir(root_folder):
        file_path = os.path.join(root_folder, filename)
        if os.path.isfile(file_path) and filename.endswith((".chd", ".iso", ".rvz")):
            match = re.search(r"\(Disc (\d)\)", filename)
            if match and 1 <= int(match.group(1)) <= 9:
                name = " ".join(filename.split(" (Disc")[0].split(" ")[:-1])
                disc_groups[name].append(filename)

    # Move files to MultiDisc folder
    moved_files = []
    for name, discs in disc_groups.items():
        for disc in discs:
            source_path = os.path.join(root_folder, disc)
            destination_path = os.path.join(multi_disc_folder, disc)

            # Check if the source and destination paths are not directories and not the same
            if not os.path.isdir(source_path) and source_path != destination_path:
                shutil.move(source_path, destination_path)
                moved_files.append(destination_path)

    # Create m3u file in root folder
    m3u_files_created = []
    for name, discs in disc_groups.items():
        m3u_filename = f"{name} (MultiDisc).m3u"
        m3u_path = os.path.join(root_folder, m3u_filename)

        # Check if M3U file already exists
        if not os.path.exists(m3u_path):
            # Create m3u file
            with open(m3u_path, 'a') as m3u_file:
                for disc in discs:
                    if disc.endswith(".rvz"):
                        m3u_file.write(f".\\MultiDisc\\{disc}\n")
                    else:
                        m3u_file.write(f"\\MultiDisc\\{disc}\n")
            m3u_files_created.append(m3u_path)

    # Write log file
    with open(log_file, 'w') as log:
        log.write("Moved files:\n")
        for file_path in moved_files:
            log.write(f"{file_path}\n")
        log.write("\nCreated/Checked m3u files:\n")
        for m3u_path in m3u_files_created:
            log.write(f"{m3u_path}\n")

if __name__ == "__main__":
    script_folder = os.path.dirname(os.path.realpath(__file__))
    move_files_and_create_m3u(script_folder)
