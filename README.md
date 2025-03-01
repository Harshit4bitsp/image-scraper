# HTML Image Scraper

A desktop application for extracting and downloading images from HTML content. This tool allows you to paste HTML code, specify an image class filter, and download all matching images to a directory of your choice.

![HTML Image Scraper screenshot](https://github.com/yourusername/html-image-scraper/raw/main/screenshot.png)

## Features

- User-friendly GUI interface
- Extract images by CSS class (optional)
- Choose custom output directory
- Real-time download progress logging
- Automatic retry mechanism for failed downloads
- Multi-threaded downloads to keep UI responsive
- Handles URLs with different formats (including protocol-relative URLs)

## Requirements

- Python 3.6+
- tkinter (included in standard Python installation)
- beautifulsoup4
- requests

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/html-image-scraper.git

# Navigate to the directory
cd html-image-scraper

# Install requirements
pip install -r requirements.txt

# Run the application
python image_scraper.py
```

## Usage

1. Launch the application using `python image_scraper.py`
2. Paste your HTML content into the top text area
3. Specify the output directory (defaults to Desktop)
4. Optionally modify the image class filter (defaults to "origin_image")
5. Click "Download Images" to start the process
6. Monitor download progress in the bottom log area

## How It Works

The application performs the following steps:

1. Parses the HTML content using BeautifulSoup
2. Finds all image tags matching the specified class (if provided)
3. Extracts image URLs from "src" or "data-original" attributes
4. Downloads each image to the selected directory
5. Provides real-time feedback about the download process

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.