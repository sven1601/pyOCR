import subprocess
import os
import sys

inputDir = ""
pdfFileList = []
ocrCommand = ["ocrmypdf", "-l", "deu+eng", "--output-type", "pdfa"]
ocrCommand_tmp = []
gsCommand = ["gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-dNOPAUSE", "-dBATCH"]
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
    totalLength = 150
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

    if len(sys.argv) != 3 or (int(sys.argv[2]) < 1 or int(sys.argv[2]) > 3):
        print('Usage: pyOCR.py [InputDir] [Quality]')
        print('InutDir: Whole folder to convert')
        print('Quality: 1 - 3 (72dpi, 150dpi, 300dpi)')
        return

    inputDir = sys.argv[1] 
    #inputDir = '/home/sven/Temp'       # Debug Mode
    quality = int(sys.argv[2])
    #quality = 2                        # Debug Mode

    if os.path.isdir(inputDir) == False:
        print('Input Dir (Param 1) doesn\'t exist, please check params!!!')
        return

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
        outputFile = os.path.join(inputDir, filename + "_out.pdf")
            
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

            gsCommand_tmp.append("-sOutputFile=" + outputFile)
            gsCommand_tmp.append(outputFileTmp)       
            result = subprocess.run(gsCommand_tmp, capture_output=True)     #Input File

            if result.returncode == 0:
                counter += 1
                printProgressBar(counter, items)
                os.remove(outputFileTmp)                
            else:
                print("Ghostscript Returncode: " + str(result) + "on file: " + filenameWithExt)
                return
        else:
            print("OCRmyPDF Returncode: " + str(result) + "on file: " + filenameWithExt)
            return

    clear() 

# ----------------------------------------------------------
main()             
