# Image Batch Renamer

A Python desktop application that helps you organize your image collections by automatically renaming files in bulk. It's particularly useful for photographers and digital artists who need to organize large collections of images across multiple directories.

## Features

- 🖼️ Supports multiple image formats (PNG, JPG, JPEG, GIF, BMP, WEBP)
- 📁 Processes all subdirectories automatically
- 🏷️ Names files based on their directory names or custom prefixes
- 🔢 Adds sequential numbering with optional leading zeros (1-10 digits)
- 🔄 Multiple sorting options:
  - Sort by name (natural sorting)
  - Sort by creation date
  - Sort by modified date
  - Ascending or descending order
- ⚡ Fast batch processing with error handling
- 🛡️ Safe renaming with automatic rollback on errors
- 🎨 Modern and user-friendly GUI

## Screenshots

![Screenshot 2025-05-13 210042](https://github.com/user-attachments/assets/67085112-d719-48c9-a7e9-87d99d61f9ed)

## Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package installer)

### Required Python Packages
- tkinter (usually comes with Python)
- natsort (for natural sorting)
- pathlib (usually comes with Python)

### Steps

1. Clone the repository:
   ```cmd
   git clone https://github.com/deanFL0/image-batch-renamer.git
   cd image-batch-renamer
   ```

2. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```cmd
   python main.py
   ```

2. Using the application:
   - Click "Browse" to select a directory containing images
   - Choose whether to use directory names or a custom prefix
   - Configure numbering options:
     - Enable "Use leading zeros" if you want numbers like 001, 002, etc.
     - Set the width of numbers (1-10 digits)
     - Set a starting number if needed
     - Choose whether to continue numbering across folders
   - Select sorting options:
     - Sort by: Name, Creation Date, or Modified Date
     - Sort direction: Ascending or Descending
   - Click "Rename" to process the files

### Example

If you have a directory structure like this:
```
Photos/
  ├── Vacation2023/
  │   ├── IMG_1234.jpg
  │   ├── IMG_1235.jpg
  │   └── IMG_1236.jpg
  └── Birthday/
      ├── DSC_001.jpg
      └── DSC_002.jpg
```

After processing with default settings, it will become:
```
Photos/
  ├── Vacation2023/
  │   ├── Vacation2023-1.jpg
  │   ├── Vacation2023-2.jpg
  │   └── Vacation2023-3.jpg
  └── Birthday/
      ├── Birthday-1.jpg
      └── Birthday-2.jpg
```

Or with leading zeros (width=7) enabled:
```
Photos/
  ├── Vacation2023/
  │   ├── Vacation2023-0000001.jpg
  │   ├── Vacation2023-0000002.jpg
  │   └── Vacation2023-0000003.jpg
  └── Birthday/
      ├── Birthday-0000001.jpg
      └── Birthday-0000002.jpg
```

## Project Structure

```
image-batch-renamer/
├── gui/               # User interface components
│   ├── app_window.py  # Main application window
│   └── message_popup.py # Popup dialogs
├── utils/             # Utility modules
│   ├── renamer.py     # File renaming logic
│   └── validators.py  # Input validation
├── main.py           # Application entry point
└── requirements.txt  # Python dependencies
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. When contributing:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Natural sorting provided by the [natsort](https://github.com/SethMMorton/natsort) library
- Built with Python's tkinter for cross-platform compatibility
