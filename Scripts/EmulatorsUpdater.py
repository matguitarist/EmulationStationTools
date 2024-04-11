import subprocess
import os

def update_emulators():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    emulator_folder = os.path.join(script_dir, 'emulators').replace("\\", "/")
    print("Updater script directory:", script_dir)
    print("Emulator folder:", emulator_folder)

    scripts = [
        os.path.join(emulator_folder, "citra", "Citra Nightly Downloader.py").replace("\\", "/"),
        os.path.join(emulator_folder, "citra-canary", "Citra Canary Downloader.py").replace("\\", "/"),
        os.path.join(emulator_folder, "cxbx-reloaded", "Cxbx Downloader.py").replace("\\", "/"),
        os.path.join(emulator_folder, "xenia-canary", "Xenia-Canary-Updater.py").replace("\\", "/")
    ]

    for script in scripts:
        folder, filename = os.path.split(script)
        print(f"Running {filename} in {folder}...")

        try:
            os.chdir(folder)  # Change the current working directory
            print(f"Current directory changed to: {os.getcwd()}")

            # Construct the command to launch the script with 'py'
            command = f'py "{filename}"'
            print(f"Command: {command}")

            # Launch the subprocess using subprocess.Popen
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            
            if stdout:
                print(f"Output of {filename}:\n{stdout}\n")
            elif stderr:
                print(f"Error running {filename}:\n{stderr}\n")
            else:
                print(f"No output produced by {filename}.\n")
                
            print(f"Script {filename} ran successfully.\n")

        except Exception as e:
            print(f"Error running {filename}: {str(e)}\n")
        finally:
            os.chdir(script_dir)  # Revert to the original directory
            print(f"Current directory reverted to: {os.getcwd()}")

if __name__ == "__main__":
    update_emulators()
