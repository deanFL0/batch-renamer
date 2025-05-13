"""
Validation functions for the image batch renamer application.
"""

import pathlib as p

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
    
def validate_leading_zeros(P):
    """Validate leading zeros input"""
    if P == "":  # Allow empty field
        return True
    try:
        value = int(P)
        return value >= 1 and value <= 10
    except ValueError:
        return False

def validate_directory(directory_path: str) -> tuple[bool, str]:
    """
    Validate if the directory path exists, is accessible, and contains image files.
    
    Args:
        directory_path: Path to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
            - is_valid: True if directory exists and contains at least one image
            - error_message: Empty string if valid, otherwise contains error description
    """
    # Check if directory path is provided
    if not directory_path:
        return False, "Please select a directory."

    # Check if directory exists and is accessible
    if not p.Path(directory_path).is_dir():
        return False, f"The path '{directory_path}' is not a valid directory."
        
    # Check if directory contains any images (including in subdirectories)
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
    has_files = False
    has_images = False
    
    for root, _, files in p.Path(directory_path).walk():
        if files:  # Directory has at least one file
            has_files = True
            # Check if any file is an image
            if any(p.Path(file).suffix.lower() in image_extensions for file in files):
                has_images = True
                break
    
    if not has_files:
        return False, f"The directory '{directory_path}' is empty."
    
    if not has_images:
        return False, f"No image files found in '{directory_path}' or its subdirectories.\nSupported formats: {', '.join(sorted(ext[1:] for ext in image_extensions))}"
    
    return True, ""