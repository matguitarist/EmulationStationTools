import os
import tkinter as tk
from tkinter import filedialog, messagebox

class RomCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rom Checker")

        # Set dark mode color scheme
        self.root.tk_setPalette(background='#1e1e1e', foreground='#ffffff', activeBackground='#333333', activeForeground='#ffffff')

        self.root_folder_var = tk.StringVar()
        self.cfg_file_var = tk.StringVar()
        self.rom_list_var = tk.StringVar()
        self.collection_path_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Select Root Folder
        root_folder_label = tk.Label(self.root, text="Select Root Folder (Containing ROMs):", bg='#1e1e1e', fg='#ffffff')
        root_folder_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        root_folder_entry = tk.Entry(self.root, textvariable=self.root_folder_var, width=50, bg='#333333', fg='#ffffff', insertbackground='#ffffff')
        root_folder_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        root_folder_button = tk.Button(self.root, text="Browse", command=self.select_root_folder, bg='#333333', fg='#ffffff', activebackground='#555555', activeforeground='#ffffff')
        root_folder_button.grid(row=0, column=2, padx=10, pady=10)

        # Select CFG File
        cfg_file_label = tk.Label(self.root, text="Select CFG File:", bg='#1e1e1e', fg='#ffffff')
        cfg_file_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.cfg_file_dropdown = tk.OptionMenu(self.root, self.cfg_file_var, "")
        self.cfg_file_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Select ROM List Button
        rom_list_button = tk.Button(self.root, text="Select ROM List", command=self.select_rom_list, bg='#333333', fg='#ffffff', activebackground='#555555', activeforeground='#ffffff')
        rom_list_button.grid(row=2, column=2, padx=10, pady=10)

        # ROM List
        rom_list_label = tk.Label(self.root, text="ROM List:", bg='#1e1e1e', fg='#ffffff')
        rom_list_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        rom_list_entry = tk.Entry(self.root, textvariable=self.rom_list_var, width=50, bg='#333333', fg='#ffffff', insertbackground='#ffffff')
        rom_list_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Collection Path Label
        collection_path_label = tk.Label(self.root, text="Collection Path:", bg='#1e1e1e', fg='#ffffff')
        collection_path_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        collection_path_entry = tk.Entry(self.root, textvariable=self.collection_path_var, width=50, bg='#333333', fg='#ffffff', insertbackground='#ffffff')
        collection_path_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        collection_path_entry.config(state='readonly')  # Make it read-only

        # Check ROMs Button
        check_roms_button = tk.Button(self.root, text="Check ROMs", command=self.check_roms, bg='#333333', fg='#ffffff', activebackground='#555555', activeforeground='#ffffff')
        check_roms_button.grid(row=3, column=1, pady=20)

    def select_root_folder(self):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            self.root_folder_var.set(selected_folder)
            self.update_cfg_file_dropdown(selected_folder)
            self.rom_list_var.set("")  # Clear the ROM list path

    def update_cfg_file_dropdown(self, root_folder):
        collections_folder = os.path.join(root_folder, "emulationstation", ".emulationstation", "collections")
        cfg_files = [f for f in os.listdir(collections_folder) if f.endswith(".cfg")]

        self.cfg_file_var.set("")  # Clear the current selection

        menu = self.cfg_file_dropdown["menu"]
        menu.delete(0, 'end')

        for cfg_file in cfg_files:
            menu.add_command(label=cfg_file, command=lambda file=cfg_file: self.update_collection_path(root_folder, cfg_file))

    def select_rom_list(self):
        rom_list_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if rom_list_path:
            self.rom_list_var.set(rom_list_path)

    def update_collection_path(self, root_folder, cfg_file):
        collections_folder = os.path.join(root_folder, "emulationstation", ".emulationstation", "collections")
        collection_path = os.path.join(collections_folder, cfg_file)
        self.collection_path_var.set(collection_path)

        # Read ROM list from the CFG file
        rom_list = self.read_rom_list_from_cfg(collection_path)
        if rom_list:
            self.rom_list_var.set(rom_list)

    def read_rom_list_from_cfg(self, cfg_file_path):
        try:
            with open(cfg_file_path, 'r') as cfg_file:
                lines = cfg_file.readlines()
                rom_list = [line.strip() for line in lines if line.strip().startswith('./')]
            return rom_list
        except Exception as e:
            print(f"Error reading ROM list from CFG file: {e}")
            return None

    def check_roms(self):
        root_folder = self.root_folder_var.get()
        cfg_file = self.cfg_file_var.get()
        rom_list_path = self.rom_list_var.get()

        if not os.path.isdir(root_folder) or not os.path.isfile(rom_list_path):
            messagebox.showerror("Error", "Invalid folder or ROM list file path.")
            return

        with open(rom_list_path, "r") as file:
            roms_to_check = [line.strip() for line in file.readlines() if line.strip()]

        # Adjust paths in the ROM list if needed
        roms_to_check_adjusted = [self.adjust_path(root_folder, rom) for rom in roms_to_check]

        missing_roms = [rom for rom in roms_to_check_adjusted if not os.path.isfile(rom)]

        if missing_roms:
            messagebox.showwarning("Missing ROMs", f"The following ROMs are missing:\n\n{', '.join(missing_roms)}")
        else:
            messagebox.showinfo("All ROMs Found", "All ROMs are present in the specified folder.")

    def adjust_path(self, root_folder, rom_path):
        # Modify this function based on your path adjustment requirements
        return os.path.join(root_folder, rom_path[3:-1]) if rom_path.startswith("{./") else os.path.join(root_folder, rom_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = RomCheckerApp(root)
    root.mainloop()
