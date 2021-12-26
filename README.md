# pyOCR
Reads a folder with PDF files, adds a ocr text layer to each file and exports each file with the specified quality settings in the same folder as a "_out.pdf" file.
Tested with Python 3.8.6

## Requirements:

* tesseract + language of choice
* ocrmypdf (maybe via pip)
* ghostscript

## Usage:

python pyOCR.py [inputFolder] [quality] [outputFolder] [language]

## Parameters:

* inputFolder:    
  * Folder which contains the pdf files
* quality:        
  * 1 = GhostScript Quality "Screen" 72dpi
  * 2 = GhostScript Quality "EBook" 150dpi
  * 3 = GhostScript Quality "Printer" 300dpi
  * 4 = GhostScript Quality "Pre Press" 300dpi HQ
                
## Exmaple:

python pyOCR.py ~/tmp/ 2 ~/Documents/ deu+eng
