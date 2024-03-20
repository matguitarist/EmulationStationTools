import os
import shutil
import tkinter as tk
from tkinter import filedialog

def add_suffix_to_files(folder_path, suffix, target_folder):
    # ... (same code as before)

def remove_empty_folders(base_folder):
    # ... (same code as before)

def execute_script():
    root_folder = filedialog.askdirectory(title="Select Root Folder")
    
    if not root_folder:
        return  # User canceled the folder selection

    # Add the desired suffix based on folder name
    folders_to_suffix = {
        "artwork_3d": ("-boxart", "images"),
        "artwork_front": ("-thumb", "images"),
        "fanart": ("-fanart", "images"),
        "logo": ("-marquee", "images"),
        "medium_front": ("-cartridge", "images"),
        "medium_disc": ("-cartridge", "images"),
        "video": ("", "videos")
    }

    for folder_name, (suffix, target_folder) in folders_to_suffix.items():
        folder_path_with_suffix = os.path.join(root_folder, folder_name)
        if os.path.exists(folder_path_with_suffix):
            add_suffix_to_files(folder_path_with_suffix, suffix, target_folder)
        else:
            print(f"Skipping folder: {folder_name} as it doesn't exist.")

    # Remove empty folders
    remove_empty_folders(root_folder)

    print("Script execution complete")

# Create the main application window
app = tk.Tk()
app.title("File Renamer and Mover")

# Add a button to execute the script
execute_button = tk.Button(app, text="Execute Script", command=execute_script)
execute_button.pack(pady=20)

# Add a toggle button for light and dark mode
mode_variable = tk.StringVar()
mode_variable.set("Light Mode")

def toggle_mode():
    current_mode = mode_variable.get()
    if current_mode == "Light Mode":
        app.configure(bg="white")
        execute_button.configure(bg="lightgray")
        mode_variable.set("Dark Mode")
    else:
        app.configure(bg="black")
        execute_button.configure(bg="darkgray", fg="white")
        mode_variable.set("Light Mode")

mode_button = tk.Button(app, textvariable=mode_variable, command=toggle_mode)
mode_button.pack(side="top", anchor="ne", padx=10, pady=10)

# Start the Tkinter event loop
app.mainloop()
