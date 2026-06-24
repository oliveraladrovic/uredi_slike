# Image Prep Tool

A small Windows desktop application for preparing product images for web upload.

The app provides a simple Tkinter GUI where the user selects a product folder, enters a product SKU and a web-ready product name, then processes all images from the product's `src` folder.

Original images are never modified. Processed images are saved in the product folder as WebP files.

## Features

* Simple Windows desktop GUI built with Tkinter
* Configurable work directory stored in `config.json`
* Product folder validation by SKU
* Image source folder validation
* Web-safe filename validation
* Supports `.jpg`, `.jpeg`, `.png`, and `.webp` source images
* Converts transparent backgrounds to white
* Resizes large images so the longest side is max 780 px
* Places each image on a centered 800x800 white canvas
* Saves processed images as `.webp`
* Continues output numbering if processed images already exist
* Does not modify original source images

## Example Folder Structure

The app expects a work directory containing product folders.

Example:

```text
products_2026/
    123456/
        src/
            original_image_1.jpg
            original_image_2.png
```

If the user enters:

```text
SKU: 123456
WEB name: APPLE iPhone 15
```

the app reads images from:

```text
products_2026/123456/src/
```

and saves processed images into:

```text
products_2026/123456/
```

Example output:

```text
APPLE iPhone 15.webp
APPLE iPhone 15_1.webp
APPLE iPhone 15_2.webp
```

## Image Processing Pipeline

Each source image goes through the following steps:

1. Open source image
2. Remove alpha channel by placing transparency on a white background
3. Resize image so the longest side is at most 780 px
4. Place resized image on a centered 800x800 white canvas
5. Save the result as a WebP file

Small images are not enlarged. For example, a 550x550 image will be centered on an 800x800 white canvas without being upscaled.

## Configuration

The application stores its work directory in a local `config.json` file.

Example:

```json
{
    "work_dir": "D:/products_2026"
}
```

The config file is created or updated through the app's settings dialog:

```text
Postavke → Osnovna mapa
```

`config.json` is intentionally not tracked by Git because it contains local machine-specific paths.

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python uredi_slike.py
```

## Requirements

The project uses:

* Python 3.12+
* Pillow
* Tkinter

Tkinter is included with most standard Python installations on Windows.

## Building a Windows EXE

Install PyInstaller:

```bash
pip install pyinstaller
```

Build the application:

```bash
pyinstaller --onedir --windowed --name UrediSlike uredi_slike.py
```

The generated application will be available in:

```text
dist/UrediSlike/
```

For distribution, copy the entire `dist/UrediSlike` folder, not only the `.exe` file.

## Notes

This tool was built as a practical desktop automation project for repetitive product image preparation. It focuses on a simple workflow, clear validation messages, and safe handling of source files.

The project is intentionally small and does not use a database, web framework, or complex architecture.
