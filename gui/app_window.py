import tkinter as tk
from tkinter import filedialog
import threading
import os
from utils.renamer import ImageRenamer
from utils.validators import validate_start_number, validate_directory
from .message_popup import MessagePopup

class AppWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Batch Image Rename")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=1)
        
        self.renamer = ImageRenamer()
        
        # Variables
        self.directory = tk.StringVar()
        self.use_custom_name = tk.BooleanVar(value=False)
        self.custom_name = tk.StringVar()
        self.use_leading_zeros = tk.BooleanVar(value=False)
        self.start_number = tk.StringVar(value="1")
        
        self._create_directory_frame()
        self._create_custom_name_frame()
        self._create_numbering_frame()
        self._create_bottom_frame()
        
        # Set minimum window size
        self.window.minsize(400, 300)

    def _create_directory_frame(self):
        frame = tk.LabelFrame(self.window, text="Directory Selection")
        frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        directory_entry = tk.Entry(frame, textvariable=self.directory)
        directory_entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        tk.Button(frame, text="Browse", width=10, 
                 command=self._browse_directory).grid(row=0, column=1, padx=5, pady=5)

    def _create_custom_name_frame(self):
        frame = tk.LabelFrame(self.window, text="Custom Name Options")
        frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(1, weight=1)

        tk.Checkbutton(frame, text="Use custom name", 
                      variable=self.use_custom_name,
                      command=self._toggle_custom_name_entry).grid(row=0, column=0, padx=5, pady=5)

        self.custom_name_entry = tk.Entry(frame, textvariable=self.custom_name, state='disabled')
        self.custom_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.use_custom_name.trace_add('write', self._toggle_custom_name_entry)

    def _create_numbering_frame(self):
        frame = tk.LabelFrame(self.window, text="Numbering Options")
        frame.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        tk.Checkbutton(frame, text="Use leading zeros in numbers (e.g., 0000001)", 
                      variable=self.use_leading_zeros).grid(row=0, column=0, 
                                                          columnspan=2, padx=5, pady=5, sticky='w')

        row1_frame = tk.Frame(frame)
        row1_frame.grid(row=1, column=0, columnspan=2, sticky='w', padx=5, pady=5)

        tk.Label(row1_frame, text="Start numbering from:").pack(side='left')
        vcmd = (self.window.register(self._validate_start_number), '%P')
        start_number_entry = tk.Entry(
            row1_frame, textvariable=self.start_number,
            validate='key', validatecommand=vcmd, width=10)
        start_number_entry.pack(side='left', padx=(5, 0))

    def _create_bottom_frame(self):
        frame = tk.Frame(self.window)
        frame.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        self.rename_btn = tk.Button(frame, text="Rename", width=20, 
                                  command=self._start_renaming)
        self.rename_btn.grid(row=0, column=0, pady=10)

        self.loading_spinner = tk.Label(frame, text="", font=('Helvetica', 12))
        self.loading_spinner.grid(row=1, column=0, pady=5)

    def _browse_directory(self):
        dir = filedialog.askdirectory()
        self.directory.set(dir)

    def _validate_start_number(self, P):
        return validate_start_number(P)

    def _toggle_custom_name_entry(self, *args):
        if self.use_custom_name.get():
            self.custom_name_entry.config(state='normal')
        else:
            self.custom_name_entry.config(state='disabled')

    def _start_renaming(self):
        # First validate the directory
        is_valid, error_message = validate_directory(self.directory.get())
        if not is_valid:
            MessagePopup.show_error(error_message, self.window)
            return

        self.loading_spinner.config(text="Renaming...")
        self.rename_btn.config(state='disabled')  # Disable button while processing
        threading.Thread(target=self._rename_thread).start()

    def _rename_thread(self):
        try:
            self.renamer.rename_files(
                self.directory.get(),
                self.use_leading_zeros.get(),
                self.use_custom_name.get(),
                self.custom_name.get(),
                self.start_number.get()
            )
        finally:
            # Always clean up UI state when done
            self.window.after(0, self._cleanup_after_rename)

    def _cleanup_after_rename(self):
        self.loading_spinner.config(text="")
        self.rename_btn.config(state='normal')  # Re-enable button

    def run(self):
        self.window.mainloop()

def create_and_run_window():
    app = AppWindow()
    app.run()
