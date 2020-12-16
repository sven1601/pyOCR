# pyOCR
Reads a folder with PDF files, adds a ocr text layer to each file and exports each file with the specified quality settings in the same folder as a "_out.pdf" file.
Tested with Python 3.8.6

## Requirements:

* tesseract
* ocrmypdf
* ghostscript

## Usage:

python3 pyOCR.py [inputFolder] [quality]

## Parameters:

* inputFolder:    
  * Folder which contains the pdf files
* quality:        
  * 1 = GhostScript Quality "Screen" 72dpi
  * 2 = GhostScript Quality "EBook" 150dpi
  * 3 = GhostScript Quality "Printer" 300dpi
                
## Exmaple:

python3 pyOCR.py ~/tmp/ 2
