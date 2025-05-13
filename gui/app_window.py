import tkinter as tk
from tkinter import filedialog
import threading
from utils.renamer import ImageRenamer
from utils.validators import validate_start_number, validate_directory, validate_leading_zeros
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
        self.start_number = tk.StringVar(value="1")
        self.continue_numbering = tk.BooleanVar(value=False)
        self.use_leading_zeros = tk.BooleanVar(value=False)
        self.number_of_leading_zeros = tk.StringVar(value="7")
        self.sort_by = tk.StringVar(value="name")
        self.sort_direction = tk.StringVar(value="asc")
        
        self._create_directory_frame()
        self._create_custom_name_frame()
        self._create_numbering_frame()
        self._create_sort_frame()
        self._create_bottom_frame()
        
        # Set minimum window size
        self.window.minsize(400, 300)

    def _create_directory_frame(self):
        frame = tk.LabelFrame(self.window, text="Directory Selection")
        frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        directory_entry = tk.Entry(frame, textvariable=self.directory)
        directory_entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        tk.Button(frame, text="Select Folder", width=10, 
                 command=self._browse_directory).grid(row=0, column=1, padx=5, pady=5)

    def _create_custom_name_frame(self):
        frame = tk.LabelFrame(self.window, text="Custom Name Options")
        frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(1, weight=1)

        tk.Checkbutton(frame, text="Use custom prefix", 
                      variable=self.use_custom_name,
                      command=self._toggle_custom_name_entry).grid(row=0, column=0, padx=5, pady=5)

        self.custom_name_entry = tk.Entry(frame, textvariable=self.custom_name, state='disabled')
        self.custom_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.use_custom_name.trace_add('write', self._toggle_custom_name_entry)

    def _create_numbering_frame(self):
        frame = tk.LabelFrame(self.window, text="Numbering Options")
        frame.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        row1_frame = tk.Frame(frame)
        row1_frame.grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=5)

        tk.Label(row1_frame, text="Start numbers from:").pack(side='left')
        vcmd = (self.window.register(validate_start_number), '%P')
        start_number_entry = tk.Entry(
            row1_frame, textvariable=self.start_number,
            validate='key', validatecommand=vcmd, width=10)
        start_number_entry.pack(side='left', padx=(5, 0))

        tk.Checkbutton(frame, text="Keep counting across folders",
                       variable=self.continue_numbering).grid(row=1, column=0, padx=5, pady=5, sticky='w', columnspan=2)

        tk.Checkbutton(frame, text="Fixed-width numbers (e.g., 001, 002, 010, 100)", 
                      variable=self.use_leading_zeros).grid(row=2, column=0, 
                                                          columnspan=2, padx=5, pady=5, sticky='w')
        
        row4_frame = tk.Frame(frame)
        row4_frame.grid(row=3, column=0, columnspan=2, sticky='w', padx=5, pady=5)

        tk.Label(row4_frame, text="Total width:").pack(side='left')
        
        # Add validation for number width entry
        leading_zeros_vcmd = (self.window.register(validate_leading_zeros), '%P')
        self.custom_leading_zeros_entry = tk.Entry(
            row4_frame, 
            textvariable=self.number_of_leading_zeros, 
            validate='key',
            validatecommand=leading_zeros_vcmd,
            width=10,
            state='disabled'
        )
        self.custom_leading_zeros_entry.pack(side='left', padx=(5, 0))
        
        tk.Label(row4_frame, text="(1-10 digits, e.g., 3 gives: 001, 4 gives: 0001)").pack(side='left', padx=(5, 0))

        self.use_leading_zeros.trace_add('write', self._toggle_custom_leading_zeros)

    def _create_sort_frame(self):
        frame = tk.LabelFrame(self.window, text="Sorting Options")
        frame.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        # Sort by criteria
        criteria_frame = tk.LabelFrame(frame, text="Sort by")
        criteria_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        
        sort_criteria = {
            "Name": "name",
            "Creation Date": "creation_date",
            "Modified Date": "modified_date"
        }
        
        for row, (text, value) in enumerate(sort_criteria.items()):
            tk.Radiobutton(criteria_frame, text=text, variable=self.sort_by, 
                        value=value).grid(row=row, column=0, padx=5, pady=1, sticky='w')

        # Sort direction
        direction_frame = tk.LabelFrame(frame, text="Order")
        direction_frame.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Radiobutton(direction_frame, text="Ascending", variable=self.sort_direction, 
                    value="asc").grid(row=0, column=0, padx=5, pady=1, sticky='w')
        tk.Radiobutton(direction_frame, text="Descending", variable=self.sort_direction, 
                    value="desc").grid(row=1, column=0, padx=5, pady=1, sticky='w')

    def _create_bottom_frame(self):
        frame = tk.Frame(self.window)
        frame.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        self.rename_btn = tk.Button(frame, text="Rename", width=20, 
                                  command=self._start_renaming)
        self.rename_btn.grid(row=0, column=0, pady=10)

        self.loading_spinner = tk.Label(frame, text="", font=('Helvetica', 12))
        self.loading_spinner.grid(row=1, column=0, pady=5)

    def _browse_directory(self):
        dir = filedialog.askdirectory()
        self.directory.set(dir)

    def _toggle_custom_name_entry(self, *args):
        if self.use_custom_name.get():
            self.custom_name_entry.config(state='normal')
        else:
            self.custom_name_entry.config(state='disabled')

    def _toggle_custom_leading_zeros(self, *args):
        if self.use_leading_zeros.get():
            self.custom_leading_zeros_entry.config(state='normal')
        else:
            self.custom_leading_zeros_entry.config(state='disabled')

    def _start_renaming(self):
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
                self.start_number.get(),
                self.continue_numbering.get(),
                self.number_of_leading_zeros.get(),
                self.sort_by.get(),
                self.sort_direction.get(),
            )
        finally:
            self.window.after(0, self._cleanup_after_rename)

    def _cleanup_after_rename(self):
        self.loading_spinner.config(text="")
        self.rename_btn.config(state='normal')  # Re-enable button

    def run(self):
        self.window.mainloop()

def create_and_run_window():
    app = AppWindow()
    app.run()
