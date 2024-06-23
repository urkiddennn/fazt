import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Fazt  File")

        self.path_var = tk.StringVar()

        self.create_widgets()
        self.update_file_list(os.getcwd())

    def create_widgets(self):
        self.root.configure(bg='#181823')

        main_frame = tk.Frame(self.root, bg='#181823')
        main_frame.pack(fill=tk.BOTH, expand=True)

        path_frame = tk.Frame(main_frame, bg='#181823')
        path_frame.pack(fill=tk.X)

        back_button = tk.Button(path_frame, text="Back", command=self.go_back, bg='#181823', fg='white', relief=tk.FLAT)
        back_button.pack(side=tk.LEFT, padx=5, pady=5)

        path_entry = tk.Entry(path_frame, textvariable=self.path_var, bg='#181823', fg='white', insertbackground='white')
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        browse_button = tk.Button(path_frame, text="Browse", command=self.browse_directory, bg='#181823', fg='white', relief=tk.FLAT)
        browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.file_listbox = tk.Listbox(main_frame, selectmode=tk.EXTENDED, bg='#181823', fg='white', selectbackground='#5A72A0', selectforeground='white')
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.file_listbox.bind('<Double-1>', self.open_item)

        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox.config(yscrollcommand=scrollbar.set)

        action_frame = tk.Frame(self.root, bg='#181823')
        action_frame.pack(fill=tk.X)

        create_dir_button = tk.Button(action_frame, text="Create Directory", command=self.create_directory_dialog, bg='#181823', fg='white', relief=tk.FLAT)
        create_dir_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(action_frame, text="Delete", command=self.delete_selected, bg='#181823', fg='white', relief=tk.FLAT)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        copy_button = tk.Button(action_frame, text="Copy", command=self.copy_selected, bg='#181823', fg='white', relief=tk.FLAT)
        copy_button.pack(side=tk.LEFT, padx=5, pady=5)

        move_button = tk.Button(action_frame, text="Move", command=self.move_selected, bg='#181823', fg='white', relief=tk.FLAT)
        move_button.pack(side=tk.LEFT, padx=5, pady=5)

    def update_file_list(self, path):
        self.path_var.set(path)
        self.file_listbox.delete(0, tk.END)

        try:
            items = os.listdir(path)
            for item in items:
                self.file_listbox.insert(tk.END, item)
        except PermissionError:
            messagebox.showerror("Error", "Permission denied.")

    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir=self.path_var.get())
        if directory:
            self.update_file_list(directory)

    def go_back(self):
        current_path = self.path_var.get()
        parent_path = os.path.dirname(current_path)
        if parent_path and os.path.exists(parent_path):
            self.update_file_list(parent_path)

    def create_directory_dialog(self):
        new_dir = simpledialog.askstring("New Directory", "Enter directory name:")
        if new_dir:
            new_dir_path = os.path.join(self.path_var.get(), new_dir)
            try:
                os.makedirs(new_dir_path)
                self.update_file_list(self.path_var.get())
            except OSError as e:
                messagebox.showerror("Error", f"Failed to create directory: {e}")

    def delete_selected(self):
        selected_items = self.file_listbox.curselection()
        if not selected_items:
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected items?")
        if not confirm:
            return

        for item_idx in selected_items[::-1]:
            item = self.file_listbox.get(item_idx)
            item_path = os.path.join(self.path_var.get(), item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
            except OSError as e:
                messagebox.showerror("Error", f"Failed to delete {item}: {e}")

        self.update_file_list(self.path_var.get())

    def copy_selected(self):
        selected_items = self.file_listbox.curselection()
        if not selected_items:
            return

        destination = filedialog.askdirectory(initialdir=self.path_var.get())
        if not destination:
            return

        for item_idx in selected_items:
            item = self.file_listbox.get(item_idx)
            item_path = os.path.join(self.path_var.get(), item)
            try:
                if os.path.isdir(item_path):
                    shutil.copytree(item_path, os.path.join(destination, item))
                else:
                    shutil.copy2(item_path, destination)
            except OSError as e:
                messagebox.showerror("Error", f"Failed to copy {item}: {e}")

    def move_selected(self):
        selected_items = self.file_listbox.curselection()
        if not selected_items:
            return

        destination = filedialog.askdirectory(initialdir=self.path_var.get())
        if not destination:
            return

        for item_idx in selected_items:
            item = self.file_listbox.get(item_idx)
            item_path = os.path.join(self.path_var.get(), item)
            try:
                shutil.move(item_path, destination)
            except OSError as e:
                messagebox.showerror("Error", f"Failed to move {item}: {e}")

        self.update_file_list(self.path_var.get())

    def open_item(self, event):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_item = self.file_listbox.get(selected_index[0])
            selected_path = os.path.join(self.path_var.get(), selected_item)
            if os.path.isdir(selected_path):
                self.update_file_list(selected_path)
            else:
                try:
                    if selected_item.endswith(('.doc', '.docx')):
                        subprocess.Popen(['start', '', selected_path], shell=True)
                    elif selected_item.endswith('.ppt'):
                        subprocess.Popen(['start', '', selected_path], shell=True)
                    else:
                        subprocess.Popen(['notepad.exe', selected_path])
                except OSError as e:
                    messagebox.showerror("Error", f"Failed to open {selected_item}: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManager(root)
    root.geometry("600x400")
    root.mainloop()
