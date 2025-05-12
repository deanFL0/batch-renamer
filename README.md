# Image Batch Renamer

A Python desktop application that helps you organize your image collections by automatically renaming files in bulk. It's particularly useful for photographers and digital artists who need to organize large collections of images across multiple directories.

## Features

- 🖼️ Supports multiple image formats (PNG, JPG, JPEG, GIF, BMP, WEBP)
- 📁 Processes all subdirectories automatically
- 🏷️ Names files based on their directory names or custom prefixes
- 🔢 Adds sequential numbering with optional leading zeros
- 🔄 Natural sorting for consistent ordering
- ⚡ Fast batch processing with error handling
- 🛡️ Safe renaming with automatic rollback on errors
- 🎨 Modern and user-friendly GUI

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Steps

1. Clone the repository:
   ```cmd
   git clone https://github.com/yourusername/image-batch-renamer.git
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
   - Enable "Use leading zeros" if you want numbers like 001, 002, etc.
   - Set a starting number if needed
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
      ├── Birthday-4.jpg
      └── Birthday-5.jpg
```

Or with leading zeros enabled:
```
Photos/
  ├── Vacation2023/
  │   ├── Vacation2023-0000001.jpg
  │   ├── Vacation2023-0000002.jpg
  │   └── Vacation2023-0000003.jpg
  └── Birthday/
      ├── Birthday-0000004.jpg
      └── Birthday-0000005.jpg
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

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Natural sorting provided by the [natsort](https://github.com/SethMMorton/natsort) library
- Built with Python's tkinter for cross-platform compatibility
