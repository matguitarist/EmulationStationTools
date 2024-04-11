import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tqdm import tqdm
from threading import Thread

class CustomCollectionGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Custom Collection Generator")

        # Get the directory of the script
        self.root_folder = os.path.dirname(__file__)

        # Set paths for the collection and ROMs folders
        self.collection_folder = os.path.join(self.root_folder, "emulationstation", ".emulationstation", "collections")
        self.roms_folder = os.path.join(self.root_folder, "roms")

        # GUI setup
        self.collection_label = ttk.Label(master, text="Select Custom Collection:")
        self.collection_label.pack(pady=10)

        self.collection_var = tk.StringVar()
        self.collection_dropdown = ttk.Combobox(master, textvariable=self.collection_var, postcommand=self.update_collection_dropdown)
        self.collection_dropdown.pack(pady=10)

        self.collection_count_label = ttk.Label(master, text="Number of Games:")
        self.collection_count_label.pack(pady=5)

        self.new_collection_label = ttk.Label(master, text="Create New Collection:")
        self.new_collection_label.pack(pady=10)

        self.new_collection_entry = ttk.Entry(master)
        self.new_collection_entry.pack(pady=10)

        self.create_collection_button = ttk.Button(master, text="Create New Collection", command=self.create_new_collection)
        self.create_collection_button.pack(pady=10)

        self.search_label = ttk.Label(master, text="Enter Keyword to Search:")
        self.search_label.pack(pady=10)

        self.search_entry = ttk.Entry(master)
        self.search_entry.pack(pady=10)

        self.extensions_label = ttk.Label(master, text="Enter Extensions (comma-separated):")
        self.extensions_label.pack(pady=10)

        # Make the "Enter Extensions" box wider
        self.extensions_entry = ttk.Entry(master, width=50)
        self.extensions_entry.insert(0, ".zip,.7z,.chd,.iso,.cso,.wad,.rvz,.sfc,.3ds,.nsp,.xci,.m3u,.z64,.zar,.bat")
        self.extensions_entry.pack(pady=10)

        self.search_button = ttk.Button(master, text="Search", command=self.search_and_update_collection)
        self.search_button.pack(pady=20)

        self.progress_bar = ttk.Progressbar(master, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.pack(pady=10)

        self.roms_path_label = ttk.Label(master, text=f"ROMs Folder Path: {self.roms_folder}")
        self.roms_path_label.pack(pady=5)

        self.collection_path_label = ttk.Label(master, text=f"Collection Folder Path: {self.collection_folder}")
        self.collection_path_label.pack(pady=5)

        # Bind refresh action to dropdown menu selection
        self.collection_dropdown.bind("<<ComboboxSelected>>", self.update_collection_count)

    def update_collection_dropdown(self):
        # List all .cfg files in the collection folder and sort them
        collection_files = sorted([f for f in os.listdir(self.collection_folder) if f.endswith(".cfg")])
        self.collection_dropdown['values'] = collection_files

    def update_collection_count(self, event=None):
        selected_collection = self.collection_var.get()
        if selected_collection:
            collection_path = os.path.join(self.collection_folder, selected_collection)
            try:
                with open(collection_path, 'r') as collection_file:
                    lines = collection_file.readlines()
                    num_games = len(lines)
                    self.collection_count_label.config(text=f"Number of Games: {num_games}")
            except FileNotFoundError:
                self.collection_count_label.config(text="Number of Games: N/A")

    def search_and_update_collection(self):
        selected_collection = self.collection_var.get()
        new_collection_name = self.new_collection_entry.get()
        keyword = self.search_entry.get()
        extensions = [ext.strip() for ext in self.extensions_entry.get().split(",")]

        if not selected_collection and not new_collection_name:
            messagebox.showerror("Error", "Please select an existing collection or enter a name for a new one.")
            return

        if new_collection_name:
            selected_collection = f"custom-{new_collection_name}.cfg"

        collection_path = os.path.join(self.collection_folder, selected_collection)

        existing_lines = set()  # To keep track of existing lines in the collection

        # Read existing lines in the collection file
        try:
            with open(collection_path, 'r') as collection_file:
                existing_lines = {line.strip() for line in collection_file}
        except FileNotFoundError:
            pass  # Collection file might not exist yet

        # Get the total number of files to search
        total_files = sum(len(files) for _, _, files in os.walk(self.roms_folder))

        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = total_files

        def search_files():
            with tqdm(total=total_files, desc='Searching ROMs', unit='file(s)', ascii=True) as pbar:
                with open(collection_path, 'a') as collection_file:
                    for root, dirs, files in os.walk(self.roms_folder):
                        for file in files:
                            if file.endswith(tuple(extensions)) and keyword.lower() in file.lower():
                                # Use relative path with forward slashes and ./ before roms/
                                rom_path = os.path.relpath(os.path.join(root, file), self.root_folder).replace("\\", "/")
                                game_name = os.path.splitext(os.path.basename(file))[0]
                                if "MultiDisc" not in rom_path and f"./{rom_path}" not in existing_lines:
                                    collection_file.write(f"./{rom_path}\n")
                                    existing_lines.add(f"./{rom_path}")
                                pbar.update(1)
                                self.progress_bar['value'] += 1
            self.progress_bar['value'] = 0
            self.update_collection_count()
            messagebox.showinfo("Success", f"Collection '{selected_collection}' updated successfully.")

        Thread(target=search_files).start()

    def create_new_collection(self):
        new_collection_name = self.new_collection_entry.get()
        if new_collection_name:
            new_collection_file = f"custom-{new_collection_name}.cfg"
            new_collection_path = os.path.join(self.collection_folder, new_collection_file)

            if os.path.exists(new_collection_path):
                messagebox.showerror("Error", "Collection file already exists. Choose a different name.")
                return

            with open(new_collection_path, 'w'):
                pass  # Create an empty file

            messagebox.showinfo("Success", f"Collection '{new_collection_name}' created successfully.")
            self.update_collection_dropdown()
        else:
            messagebox.showerror("Error", "Please enter a name for the new collection.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomCollectionGenerator(root)
    root.mainloop()
