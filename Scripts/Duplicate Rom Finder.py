import os
import tkinter as tk
from tkinter import filedialog, messagebox
import binascii

class FolderComparer:
    def __init__(self, master):
        self.master = master
        self.master.title("Folder Comparator")

        # Dark mode variables
        self.dark_mode = tk.BooleanVar()
        self.dark_mode.set(False)

        # Entry widgets to display or input folder paths
        self.folder1_entry = tk.Entry(self.master, width=50)
        self.folder1_entry.grid(row=0, column=0, padx=10, pady=10)

        self.folder2_entry = tk.Entry(self.master, width=50)
        self.folder2_entry.grid(row=1, column=0, padx=10, pady=10)

        # Buttons to select or input folders
        tk.Button(self.master, text="Select Folder 1", command=self.select_folder1).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.master, text="Select Folder 2", command=self.select_folder2).grid(row=1, column=1, padx=10, pady=10)

        # Entry for manually entering file extension
        tk.Label(self.master, text="File Extension:").grid(row=2, column=0, padx=10, pady=10)
        self.file_extension_entry = tk.Entry(self.master, width=10)
        self.file_extension_entry.insert(0, "zip")  # Default to "zip" extension
        self.file_extension_entry.grid(row=2, column=1, padx=10, pady=10)

        # Dark mode toggle
        tk.Checkbutton(self.master, text="Dark Mode", variable=self.dark_mode, command=self.toggle_dark_mode).grid(row=3, column=0, columnspan=2, pady=10)

        # Button to start comparison
        tk.Button(self.master, text="Compare Folders", command=self.compare_folders).grid(row=4, column=0, columnspan=2, pady=10)

        # Button to generate text file with duplicate paths
        tk.Button(self.master, text="Generate Duplicate File List", command=self.generate_duplicate_file_list).grid(row=5, column=0, columnspan=2, pady=10)

    def toggle_dark_mode(self):
        if self.dark_mode.get():
            self.master.configure(bg="#2E2E2E")
            for widget in self.master.winfo_children():
                widget.configure(bg="#2E2E2E", fg="white")
        else:
            self.master.configure(bg="white")
            for widget in self.master.winfo_children():
                widget.configure(bg="white", fg="black")

    def select_folder1(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder1_entry.delete(0, tk.END)
            self.folder1_entry.insert(0, folder_path)

    def select_folder2(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder2_entry.delete(0, tk.END)
            self.folder2_entry.insert(0, folder_path)

    def compare_folders(self):
        folder1_path = self.folder1_entry.get()
        folder2_path = self.folder2_entry.get()

        if not folder1_path:
            messagebox.showerror("Error", "Please select or enter Folder 1.")
            return
        if not folder2_path:
            messagebox.showerror("Error", "Please select or enter Folder 2.")
            return

        file_extension = self.file_extension_entry.get().strip()
        if not file_extension:
            messagebox.showerror("Error", "Please enter a file extension.")
            return

        duplicates = self.find_duplicates(folder1_path, folder2_path, file_extension)

        if duplicates:
            messagebox.showinfo("Duplicates Found", f"{len(duplicates)} duplicate files found.")
            for file_path, crc in duplicates:
                print(f"File: {file_path}\nCRC32: {crc:08X}\n")  # Format as hexadecimal
        else:
            messagebox.showinfo("No Duplicates", "No duplicate files found.")

    def calculate_crc32(self, file_path):
        crc = 0xFFFFFFFF  # Initial CRC value
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                crc = binascii.crc32(chunk, crc) & 0xFFFFFFFF  # Mask to keep the result as a 32-bit unsigned integer
        return crc

    def find_duplicates(self, folder1, folder2, file_extension):
        duplicates = []

        for root, _, files in os.walk(folder1):
            for file in files:
                if file.endswith(f".{file_extension}"):
                    file_path1 = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path1, folder1)
                    file_path2 = os.path.join(folder2, relative_path)

                    if os.path.exists(file_path2):
                        crc1 = self.calculate_crc32(file_path1)
                        crc2 = self.calculate_crc32(file_path2)

                        if crc1 == crc2:
                            duplicates.append((file_path1, crc1))

        return duplicates

    def generate_duplicate_file_list(self):
        folder1_path = self.folder1_entry.get()
        folder2_path = self.folder2_entry.get()

        if not folder1_path or not folder2_path:
            messagebox.showerror("Error", "Please select or enter both folders.")
            return

        file_extension = self.file_extension_entry.get().strip()
        if not file_extension:
            messagebox.showerror("Error", "Please enter a file extension.")
            return

        duplicates = self.find_duplicates(folder1_path, folder2_path, file_extension)

        if duplicates:
            try:
                with open('duplicate_files.txt', 'w') as file:
                    for file_path, crc in duplicates:
                        file.write(f"File: {file_path}\nCRC32: {crc:08X}\n\n")  # Format as hexadecimal
                messagebox.showinfo("File Created", "Duplicate file list generated in 'duplicate_files.txt'.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create file: {str(e)}")
        else:
            messagebox.showinfo("No Duplicates", "No duplicate files found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderComparer(root)
    root.mainloop()
