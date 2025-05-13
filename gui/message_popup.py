"""
Module for handling popup messages in the application.
"""
import tkinter as tk
from typing import Optional

class MessagePopup:
    DEFAULT_WIDTH = 400  # Fixed width for all popups
    
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
        
        # Configure grid
        top.grid_columnconfigure(0, weight=1)
        top.grid_rowconfigure(0, weight=1)
        
        # Create frame for content with padding
        frame = tk.Frame(top)
        frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        # Title label
        title_label = tk.Label(frame, text=title, font=('Helvetica', 12, 'bold'), fg=color)
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Message label with word wrapping
        msg_label = tk.Label(frame, text=message, wraplength=cls.DEFAULT_WIDTH - 60,
                           justify='left')  # Changed to left justify for better readability
        msg_label.grid(row=1, column=0, pady=(0, 20), sticky='nsew')
        
        # OK button
        btn = tk.Button(frame, text="OK", command=top.destroy, width=10)
        btn.grid(row=2, column=0)
        
        # Set initial size
        top.geometry(f"{cls.DEFAULT_WIDTH}x10")  # Start with minimal height
        
        # Update tasks and calculate required size
        top.update_idletasks()
        
        # Get the required height based on the content
        required_height = frame.winfo_reqheight() + 40  # Add some padding
        
        # Set the final window size
        top.geometry(f"{cls.DEFAULT_WIDTH}x{required_height}")
        
        # Center the window on top of the parent window
        if parent:
            x = (parent.winfo_rootx() + parent.winfo_width() // 2) - cls.DEFAULT_WIDTH // 2
            y = (parent.winfo_rooty() + parent.winfo_height() // 2) - required_height // 2
            top.geometry(f'+{x}+{y}')
        
        # Make the window modal
        top.transient(parent)
        top.grab_set()
        top.focus_set()
        top.wait_window()
