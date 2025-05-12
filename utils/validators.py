"""
Validation functions for the image batch renamer application.
"""

import os

def validate_start_number(value: str) -> bool:
    """
    Validate if the input string can be converted to a positive integer.
    Empty string is considered valid.
    
    Args:
        value: String to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if value == "":  # Allow empty field
        return True
    try:
        int(value)
        return True
    except ValueError:
        return False

def validate_directory(directory_path: str) -> tuple[bool, str]:
    """
    Validate if the directory path exists and is accessible.
    
    Args:
        directory_path: Path to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not directory_path:
        return False, "Please select a valid directory."
        
    if not os.path.isdir(directory_path):
        return False, f"The path {directory_path} is not a valid directory."
        
    return True, ""
