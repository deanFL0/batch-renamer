"""
Module for handling popup messages in the application.
"""
import tkinter as tk
from typing import Optional

class MessagePopup:
    DEFAULT_WIDTH = 400  # Fixed width for all popups
    MIN_HEIGHT = 150    # Minimum height
    
    @classmethod
    def show_error(cls, message: str, parent: Optional[tk.Tk] = None):
        """
        Show an error message in a popup window.
        
        Args:
            message: The error message to display
            parent: Optional parent window
        """
        cls._show_message(message, "Error", "red", parent)
    
    @classmethod
    def show_success(cls, message: str, parent: Optional[tk.Tk] = None):
        """
        Show a success message in a popup window.
        
        Args:
            message: The success message to display
            parent: Optional parent window
        """
        cls._show_message(message, "Success", "green", parent)
    
    @classmethod
    def _show_message(cls, message: str, title: str, color: str, parent: Optional[tk.Tk] = None):
        """
        Internal method to show a message popup.
        
        Args:
            message: The message to display
            title: Title of the popup window
            color: Color of the title text
            parent: Optional parent window
        """
        top = tk.Toplevel(parent)
        top.title(title)
        
        # Make the window fixed width but adjust height based on content
        top.geometry(f"{cls.DEFAULT_WIDTH}x{cls.MIN_HEIGHT}")
        top.resizable(False, True)  # Fixed width, adjustable height
        
        # Configure grid
        top.grid_columnconfigure(0, weight=1)
        top.grid_rowconfigure(0, weight=1)
        
        # Create frame for content
        frame = tk.Frame(top)
        frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        # Title label
        title_label = tk.Label(frame, text=title, font=('Helvetica', 12, 'bold'), fg=color)
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Message label with word wrapping
        msg_label = tk.Label(frame, text=message, wraplength=cls.DEFAULT_WIDTH - 60, 
                           justify='center')
        msg_label.grid(row=1, column=0, pady=(0, 20))
        
        # OK button
        btn = tk.Button(frame, text="OK", command=top.destroy, width=10)
        btn.grid(row=2, column=0)
        
        # Center the window on screen
        top.update_idletasks()
        width = top.winfo_width()
        height = top.winfo_height()
        x = (top.winfo_screenwidth() // 2) - (width // 2)
        y = (top.winfo_screenheight() // 2) - (height // 2)
        top.geometry(f'+{x}+{y}')
        
        # Make the window modal
        top.transient(parent)
        top.grab_set()
        top.focus_set()
        top.wait_window()
