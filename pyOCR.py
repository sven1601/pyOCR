import subprocess
import os
import sys

inputDir = ""
outputDir = ""
pdfFileList = []
ocrCommand_tmp = []
gsCommand_tmp = []
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
        print('Quality:     1 - 4 (72dpi, 150dpi, 300dpi, 300dpi hq)')
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

    if quality < 1 or quality > 4:
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

    ocrCommand = ["ocrmypdf", "-l", lang, "--output-type", "pdfa", "--jobs", "4"]
    gsCommand = ["gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-dNOPAUSE", "-dBATCH"]

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
        ocrCommand_tmp.append(outputFileTmp)

        result = subprocess.run(ocrCommand_tmp, capture_output=True)

        if result.returncode == 0:
            gsCommand_tmp = []
            gsCommand_tmp = gsCommand.copy()

            if quality == 1:
                gsCommand_tmp.append('-dPDFSETTINGS=/screen')
            if quality == 2:
                gsCommand_tmp.append('-dPDFSETTINGS=/ebook')
            if quality == 3:
                gsCommand_tmp.append('-dPDFSETTINGS=/printer')
            if quality == 4:
                gsCommand_tmp.append('-dPDFSETTINGS=/prepress')

            gsCommand_tmp.append("-sOutputFile=" + outputFile)
            gsCommand_tmp.append(outputFileTmp)
            result = subprocess.run(gsCommand_tmp, capture_output=True)     #Input File

            if result.returncode == 0:
                counter += 1
                printProgressBar(counter, items)
                os.remove(outputFileTmp)
            else:
                print(f"Ghostscript Returncode: {str(result)} on file: {filenameWithExt}")
                return
        else:
            print(f"OCRmyPDF Returncode: {str(result)} on file: {filenameWithExt}")
            return

    clear()
    print(f"{str(counter)} of {str(items)} Documents successfully converted")

# ----------------------------------------------------------
main()
