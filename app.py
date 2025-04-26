import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from natsort import natsorted

def browse_directory(text):
    dir = filedialog.askdirectory()
    text.set(dir)

def validate_start_number(P):
    if P == "":  # Allow empty field
        return True
    try:
        int(P)
        return True
    except ValueError:
        return False

def rename(base_directory, use_leading_zeros, use_custom_name, custom_name, start_number):
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

    try:
        counter = int(start_number) if start_number.strip() else 1
    except ValueError:
        messagebox.showerror("Error", "Starting number must be a valid integer")
        return

    for root, subdirs, files in os.walk(base_directory):
        # Get the name of the current directory
        dir_name = os.path.basename(root)

        # Skip empty directories
        if not files:
            continue

        # Filter only image files and sort them to maintain consistent order
        image_files = natsorted([f for f in files if os.path.splitext(f)[1].lower() in image_extensions])
        
        # Skip if no image files found
        if not image_files:
            continue

        # First pass: Rename all files to temporary names to avoid conflicts
        temp_files = []
        for idx, file_name in enumerate(image_files):
            original_path = os.path.join(root, file_name)
            temp_name = f"__temp_{idx}{os.path.splitext(file_name)[1]}"
            temp_path = os.path.join(root, temp_name)
            
            try:
                os.rename(original_path, temp_path)
                temp_files.append((temp_path, file_name))
            except Exception as e:
                # If error occurs during first pass, revert any changes made
                for temp_path, original_name in temp_files:
                    try:
                        os.rename(temp_path, os.path.join(root, original_name))
                    except:
                        pass
                top = tk.Toplevel()
                top.geometry("300x120")
                tk.Label(top, text="Error renaming file: " + str(e)).pack(pady=20)
                tk.Button(top, text="OK", command=top.destroy).pack(pady=10)
                return

        # Second pass: Rename from temporary names to final names
        for temp_path, _ in temp_files:
            file_extension = os.path.splitext(temp_path)[1]

            # Determine if we should use a prefix
            if use_custom_name:
                if custom_name.strip():  # If custom name is not empty
                    prefix = f"{custom_name.strip()}-"
                else:
                    prefix = ""  # No prefix if custom name is empty
            else:
                prefix = f"{dir_name}-"  # Use directory name as prefix

            # Format new name based on user preferences
            if use_leading_zeros:
                new_name = f"{prefix}{counter:07d}{file_extension}"
            else:
                new_name = f"{prefix}{counter}{file_extension}"
                
            new_path = os.path.join(root, new_name)

            try:
                # Rename from temporary name to final name
                os.rename(temp_path, new_path)
                counter += 1
            except Exception as e:
                # If error occurs during second pass, try to clean up temporary files
                for remaining_temp, original_name in temp_files:
                    if os.path.exists(remaining_temp):
                        try:
                            os.rename(remaining_temp, os.path.join(root, original_name))
                        except:
                            pass
                top = tk.Toplevel()
                top.geometry("300x120")
                tk.Label(top, text="Error renaming file: " + str(e)).pack(pady=20)
                tk.Button(top, text="OK", command=top.destroy).pack(pady=10)
                return

    top = tk.Toplevel()
    top.geometry("300x120")
    tk.Label(top, text="Files renamed successfully").pack(pady=20)
    tk.Button(top, text="OK", command=top.destroy).pack(pady=10)

def toggle_custom_name_entry(*args):
    if use_custom_name.get():
        custom_name_entry.config(state='normal')
    else:
        custom_name_entry.config(state='disabled')

def start_renaming():
    loading_spinner.config(text="Renaming...")
    threading.Thread(target=rename, args=(directory.get(), 
                                        use_leading_zeros.get(),
                                        use_custom_name.get(),
                                        custom_name.get(),
                                        start_number.get())).start()
    loading_spinner.after(100, stop_loading_spinner)  

def stop_loading_spinner():
    if not os.path.isdir(directory.get()):  
        return
    loading_spinner.config(text="")

# main window
window = tk.Tk()
window.title("Batch Image Rename")
window.columnconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)

# Directory selection frame
frame1 = tk.LabelFrame(window, text="Directory Selection")
frame1.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
frame1.columnconfigure(0, weight=1)

directory = tk.StringVar()
directory_entry = tk.Entry(frame1, textvariable=directory)
directory_entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
tk.Button(frame1, text="Browse", width=10, command=lambda: browse_directory(directory)).grid(row=0, column=1, padx=5, pady=5)

# Custom name frame
frame2 = tk.LabelFrame(window, text="Custom Name Options")
frame2.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
frame2.columnconfigure(1, weight=1)

use_custom_name = tk.BooleanVar(value=False)
custom_name = tk.StringVar()

tk.Checkbutton(frame2, text="Use custom name", 
               variable=use_custom_name,
               command=toggle_custom_name_entry).grid(row=0, column=0, padx=5, pady=5)

custom_name_entry = tk.Entry(frame2, textvariable=custom_name, state='disabled')
custom_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

use_custom_name.trace_add('write', toggle_custom_name_entry)

# Numbering options frame
frame3 = tk.LabelFrame(window, text="Numbering Options")
frame3.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
frame3.columnconfigure(0, weight=1)

# Add checkbox for leading zeros option
use_leading_zeros = tk.BooleanVar(value=False)
tk.Checkbutton(frame3, text="Use leading zeros in numbers (e.g., 0000001)", 
               variable=use_leading_zeros).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='w')

vcmd = (window.register(validate_start_number), '%P')
start_number = tk.StringVar(value="1")

row1_frame = tk.Frame(frame3)
row1_frame.grid(row=1, column=0, columnspan=2, sticky='w', padx=5, pady=5)

tk.Label(row1_frame, text="Start numbering from:").pack(side='left')
start_number_entry = tk.Entry(
    row1_frame, textvariable=start_number,
    validate='key', validatecommand=vcmd, width=10)
start_number_entry.pack(side='left', padx=(5, 0))

# Bottom frame for rename button and loading spinner
bottom_frame = tk.Frame(window)
bottom_frame.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
bottom_frame.columnconfigure(0, weight=1)

rename_btn = tk.Button(bottom_frame, text="Rename", width=20, 
                    command=lambda: rename(directory.get(), 
                                        use_leading_zeros.get(),
                                        use_custom_name.get(),
                                        custom_name.get(),
                                        start_number.get()))
rename_btn.grid(row=0, column=0, pady=10)

loading_spinner = tk.Label(bottom_frame, text="", font=('Helvetica', 12))
loading_spinner.grid(row=1, column=0, pady=5)

# Set minimum window size
window.minsize(400, 300)

window.mainloop()
