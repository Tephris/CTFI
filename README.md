# Copy Text From Image (CTFI)

## Description
Copy Text From Image (CTFI) is a Python tool utilizing Tesseract OCR to recognize text within the area you selected on screen for Windows 10.

## Installation
Execute the following command from within the root directory to install the tool:\
`pip install .`

This will install all dependencies and also allows you to execute the tool via the command line with the command `ctfi`.

Alternatively, you can install each dependency manually. Install the required modules with the following commands:\
`pip install clipboard`\
`pip install pytesseract`\
`pip install Pillow`\
`pip install pynput`\
`pip install pywin32`

Tesseract OCR is included with this project for convenience. You can find information on it and download it yourself [here](https://github.com/tesseract-ocr/tesseract).

## Usage
Execute the tool via the command line with the command:\
`python ctfi.py` or `ctfi` if you installed using the `pip install .` command.

The tool will then prompt you to select your desired language. Enter the number corresponding to your desired language to select it.

To select an area on your screen, start at one corner of your desired area, press left-shift to begin selection, drag your mouse to the opposite corner of the area, and release left-shift.

In the event that you want to execute the tool without the red selection indicator box, you can provide `-h` or `--hide` as a command line argument to disable it. For example: `python ctfi.py -h`

## Modification
To enable copying of other languages, modify the list of tuples found at the top of `CopyTextFromImage/ctfi.py`. Specific instructions can be found as a comment within the file.

## Known Issues
- When selecting an area over Google Chrome, the screen is not properly refreshed and results in each red selection indicator box drawn to remain on screen. If you want to use this tool with Google Chrome on screen, you can disable the red selection indicator box by providing a command line argument. See Usage section above for details.