import tkinter as tk
from tkinter import filedialog
import os
import threading

def browse_directory(text):
    dir = filedialog.askdirectory()
    text.set(dir)

def rename(base_directory):
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'} 
    
    if not base_directory:
        top = tk.Toplevel()
        top.geometry("300x100")
        tk.Label(top, text="Please select a valid directory.").pack(pady=20)
        return
        
    if not os.path.isdir(base_directory):
        top = tk.Toplevel()
        top.geometry("500x100")
        tk.Label(top, text=f"The path {base_directory} is not a valid directory.").pack(pady=20)
        return

    for root, subdirs, files in os.walk(base_directory):
        if not subdirs and root == base_directory:
            continue

        subdir_name = os.path.basename(root)
        counter = 1

        for file_name in files:
            original_path = os.path.join(root, file_name)

            # Get file extension
            file_extension = os.path.splitext(file_name)[1]

            # Check if the file is an image
            if file_extension.lower() not in image_extensions:
                continue

            # Format new name
            new_name = f"{subdir_name}-{counter:07d}{file_extension}"
            new_path = os.path.join(root, new_name)

            try:
                # Rename the file
                os.rename(original_path, new_path)
                counter += 1
            except Exception as e:
                top = tk.Toplevel()
                top.geometry("300x120")
                tk.Label(top, text="Error renaming file: " + str(e)).pack(pady=20)
                tk.Button(top, text="OK", command=top.destroy).pack(pady=10)
                return

    top = tk.Toplevel()
    top.geometry("300x120")
    tk.Label(top, text="Files renamed successfully").pack(pady=20)
    tk.Button(top, text="OK", command=top.destroy).pack(pady=10)

window = tk.Tk()
window.title("Batch Image Rename")
window.geometry("400x200")

directory = tk.StringVar()
directory_entry = tk.Entry(window, textvariable=directory)
directory_entry.pack(pady=10, padx=50, fill='x')
tk.Button(window, text="Browse", width=3, command=lambda: browse_directory(directory)).pack(pady=10)

tk.Button(window, text="Rename", width=10, command=lambda: rename(directory.get())).pack(pady=10)

loading_spinner = tk.Label(window, text="", font=('Helvetica', 12))
loading_spinner.pack(pady=10)

def start_renaming():
    loading_spinner.config(text="Renaming...")
    threading.Thread(target=rename, args=(directory.get(),)).start()
    loading_spinner.after(100, stop_loading_spinner)  

def stop_loading_spinner():
    if not os.path.isdir(directory.get()):  
        return
    loading_spinner.config(text="")
window.mainloop()
