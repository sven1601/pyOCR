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
  * 0 = Lossless (Large file)
  * 1 = Try lossless
  * 2 = Medium compression
  * 3 = High compression (best filesize)
* outputFolder:
  * Folder to save the output files
* language
  * String to specify the language for tesseract and ocrmypdf, can be chained with '+'  
                
## Exmaple:

python pyOCR.py ~/tmp/ 0 ~/Documents/ deu+eng
