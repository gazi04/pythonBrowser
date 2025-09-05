# PyBrowser

A simple web browser implementation written in Python using Tkinter for the GUI and socket programming for HTTP requests.

## Overview

PyBrowser is a minimal web browser that demonstrates the core concepts of web browsing including HTTP requests, HTML parsing, and text rendering. It provides a basic GUI interface for viewing web content with scrolling capabilities.

## Features

- **HTTP/HTTPS Support**: Makes HTTP requests to web servers with support for redirects
- **HTML Parsing**: Parses HTML content and builds a document tree structure
- **Text Rendering**: Renders HTML content as formatted text with basic styling
- **GUI Interface**: Tkinter-based graphical user interface with scrolling
- **File Protocol Support**: Handles `file://` URLs for local file browsing
- **Data Protocol Support**: Basic support for `data://` URLs
- **Scrollable Content**: Mouse wheel and keyboard scrolling support

## Project Structure

```
src/
├── main.py              # Entry point and main application logic
├── config.py            # Configuration constants
├── gui/
│   └── browser.py       # Tkinter GUI implementation
├── network/
│   ├── httpClient.py    # HTTP client for making requests
│   ├── httpResponse.py  # HTTP response parsing and handling
│   └── url.py           # URL parsing and connection management
└── render/
    ├── htmlParser.py    # HTML parsing and DOM tree building
    ├── layout.py        # Text layout and formatting
    ├── render.py        # Canvas rendering engine
    ├── tag.py           # HTML tag representation
    └── text.py          # Text node representation

enums/
├── httpStatus.py        # HTTP status code definitions
└── ports.py            # Standard port definitions
```

## Core Components

### 1. Network Layer (`src/network/`)

- **`httpClient.py`**: Handles HTTP requests with redirect support and file protocol handling
- **`httpResponse.py`**: Parses HTTP responses, handles gzip compression, and tokenizes HTML content
- **`url.py`**: URL parsing, connection establishment, and protocol handling (HTTP/HTTPS/file/data)

### 2. Rendering Engine (`src/render/`)

- **`htmlParser.py`**: Parses HTML content and builds a document tree structure
- **`layout.py`**: Handles text layout, font management, and basic HTML tag formatting
- **`render.py`**: Manages canvas rendering, scrolling, and viewport management
- **`tag.py`** & **`text.py`**: Represent HTML elements and text nodes in the DOM tree

### 3. GUI (`src/gui/`)

- **`browser.py`**: Tkinter-based GUI with canvas for content display and scrollbar for navigation

## Usage

### Basic Usage

```bash
python src/main.py <URL>
```

### Examples

```bash
# Browse a website
python src/main.py https://example.com

# View a local file
python src/main.py file:///path/to/file.html

# View data URL
python src/main.py data:text/html,<h1>Hello World</h1>
```

### Programmatic Usage

```python
from src.gui.browser import Browser
from src.network.httpClient import HttpClient
from src.render.htmlParser import HtmlParser

# Create HTTP client and fetch content
client = HttpClient(max_redirects=5)
response = client.get("https://example.com")

# Parse HTML content
parser = HtmlParser(response.html_content)
dom_tree = parser.parse()

# Display in browser GUI
browser = Browser()
browser.load(response.tokenize())
```

## Configuration

The browser behavior can be customized through `src/config.py`:

- `TITLE`: Window title
- `HORIZONTAL_STEP`: Left and right margins
- `VERTICAL_STEP`: Line height and vertical margins
- `SCROLL_STEP`: Mouse wheel and keyboard scroll distance

## Supported HTML Features

The browser supports basic HTML formatting:

- **Text formatting**: Bold (`<b>`), italic (`<i>`), superscript (`<sup>`), subscript (`<sub>`)
- **Headings**: H1-H6 with different font sizes
- **Text size**: `<big>` and `<small>` tags
- **Line breaks**: `<br>` and paragraph breaks `<p>`

## Technical Details

### HTTP Implementation
- Uses raw socket programming for HTTP requests
- Supports HTTP/1.0 protocol
- Handles gzip compression
- Implements redirect following (max 5 redirects)
- SSL/TLS support for HTTPS

### HTML Parsing
- Simple tokenizer that separates HTML tags from text content
- Builds a tree structure representing the DOM
- Handles nested tags and closing tags

### Rendering
- Uses Tkinter Canvas for text rendering
- Implements word wrapping and line breaking
- Font caching for performance
- Scrollable viewport with mouse wheel support

## Dependencies

- Python 3.7+
- Tkinter (usually included with Python)
- Standard library modules: `socket`, `ssl`, `gzip`, `io`, `os`

## Limitations

- No CSS support
- No JavaScript execution
- No image rendering
- Basic HTML tag support only
- No form handling
- No cookies or session management
- Limited error handling

## Development

This is an educational project demonstrating web browser fundamentals. The code is structured to be easily understandable and extensible for learning purposes.

## License

This project is for educational purposes. Please check the license terms if you plan to use or modify this code.
