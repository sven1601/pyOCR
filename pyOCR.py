import subprocess
import os
import sys
from shutil import copyfile

inputDir = ""
outputDir = ""
pdfFileList = []
ocrCommand_tmp = []
quality = -1
clear = lambda: os.system('clear')

# ----------------------------------------------------------
def getPdfFiles(thisPath):
    for item in os.listdir(thisPath):
        file = os.path.join(thisPath, item)
        if os.path.isfile(file) and file.endswith('.pdf') and file.find("_.pdf") < 0:
            pdfFileList.append(file)
            #print(file)

    if len(pdfFileList) > 1:
        pdfFileList.sort()

# ----------------------------------------------------------
def printProgressBar(actualCount, totalCount):
    totalLength = 70
    singleStepPercent = 100 / totalLength
    if actualCount > 0:
        actualPercent = (1 / (int(totalCount) / int(actualCount))) * 100
    else:
        actualPercent = 0

    print('[', end='')

    for element in range(totalLength):
        if actualPercent > (element * singleStepPercent):
            print('#', end='')
        else:
            print(' ', end='')


    print('] ', end='')
    print('%.2f'%actualPercent + '% ' + '(Element %i '%actualCount + 'of %i)'%totalCount, end='\r')

# ----------------------------------------------------------
def main():

    clear()

    if len(sys.argv) != 5 or sys.argv[1] == "--help":
        print('-------------------------------------------------------------------------------------------------------')
        print('Usage:       pyOCR.py [InputDir] [Quality] [OutputDir] [Language]')
        print('-------------------------------------------------------------------------------------------------------')
        print('Parameters:')
        print('InutDir:     Path that conatins PDF documents to convert')
        print('Quality:     0 - 3 (Lossless, Try lossless, Medium compression, High compression)')
        print('OutputDir:   Target Output folder')
        print('Language:    String, that specifies the "3 digit letter code" for tesseract. Can be chained by \'+\'')
        print('-------------------------------------------------------------------------------------------------------')
        print('Example:     python ./pyOCR.py ~/SourceFolder/ 2 ~/TargetFolder/ deu+eng')
        print('             python ./pyOCR.py ~/SourceFolder/ 4 ~/TargetFolder/ eng')
        print('-------------------------------------------------------------------------------------------------------')
        return

    inputDir = sys.argv[1]
    quality = int(sys.argv[2])
    outputDir = sys.argv[3]
    lang = sys.argv[4]

    if quality < 0 or quality > 3:
        print('Quality (Param 2) has not a valid value, please check params!!!')
        return

    if len(inputDir) == 0 or os.path.isdir(inputDir) == False:
        print('Input Dir (Param 1) doesn\'t exist, please check params!!!')
        return

    if len(outputDir) == 0 or os.path.isdir(outputDir) == False:
        print('Output Dir (Param 3) doesn\'t exist, please check params!!!')
        return

    if len(lang) == 0:
        print('Language (Param 4) not specified, please check params!!!')
        return

    ocrCommand = ["ocrmypdf", "-l", str(lang), "--output-type", "pdfa", "--jobs", "4", "--pdfa-image-compression", "lossless", "--optimize", str(quality), "--clean"]

    getPdfFiles(inputDir)

    for file in pdfFileList:
        if "_out.pdf" in file:
            print("Please remove output files first!!!")
            return

    items = int(len(pdfFileList))
    counter = 0

    clear()
    printProgressBar(counter, items)

    for file in pdfFileList:

        filenameWithExt = os.path.basename(file)
        filename, fileExt = os.path.splitext(filenameWithExt)

        outputFileTmp = os.path.join(inputDir, filename + "_temp.pdf")
        outputFile = os.path.join(outputDir, filename + ".pdf")

        ocrCommand_tmp = []
        ocrCommand_tmp = ocrCommand.copy()
        ocrCommand_tmp.append(file)
        ocrCommand_tmp.append(outputFile)

        result = subprocess.run(ocrCommand_tmp, capture_output=True)

        if result.returncode == 0:
            counter += 1
            printProgressBar(counter, items)
        else:
            print(f"OCRmyPDF Returncode: {str(result)} on file: {filenameWithExt}")
            return

    clear()
    print(f"{str(counter)} of {str(items)} Documents successfully converted")

# ----------------------------------------------------------
main()
