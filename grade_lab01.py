# grading script for CS8 lab01, Spring 2014

from glob import glob
from shutil import copyfile
from os import remove
from os.path import isfile
import sys, subprocess
import imp
import unittest

### Some global variable definitions ### 
logFile = 'logfile.txt'
labFiles = {}           # dictionary of student names as key and list of file names as value
                        # i.e. {'John Snow': ['fileone.py', 'filetwo.py']}
labDir = sys.argv[1]    # get the name of the lab as an argument, i.e. "lab01"
labFuncsNm = labDir + "Funcs.py"
labTestsNm = labDir + "Tests.py"
testOutputDir = labDir + "TestOutput/"

def findLabFiles():
    ''' 
    Iterates through the student name directories and copies the data into the labFiles dictionary
    '''

    # glob returns all pathnames matching the specified pattern
    tmpStudents = glob("%s/*"%(labDir))
    students = []
    for student in tmpStudents:
        # do some sanity checks
        if student[0] != '_' and '.' not in student:
            # add the directories with student names into a list
            students = students + [student]

    # this loop goes through and adds a list of filenames to the associated student
    # name in the dictionary
    for student in students:
        # add each students name as a key in a dictionary
        labFiles[student] = {}

        #check if the student turned in the files in a lab directory
        fileList = []
        funcsFile=glob("%s/%s/%s"%(student, labDir, labFuncsNm))
        testsFile=glob("%s/%s/%s"%(student, labDir, labTestsNm))

        # if both files do NOT exist in the directory
        if len(funcsFile) == 0 or len(testsFile) == 0:
            fileList += []
            labFiles[student] = fileList
        # else, if both files DO exist in the directory 
        elif len(funcsFile) != 0 and len(testsFile) != 0:
            fileList += [funcsFile, testsFile]
            labFiles[student] = fileList
        # else, if one of the two is not there (this is a problem)
        else:
            fileList += []
            labFiles[student] = fileList

def cleanFiles():
    '''
    Cleans the lab files if any exist in the current directory 
    '''
    if isfile(labFuncsNm):
        remove(labFuncsNm)
    if isfile(labTestsNm):
        remove(labTestsNm)

def copyFiles(student):
    '''
    Copies the files stored in the labFiles dictionary for a given student
    Returns True if the copy was successful, False otherwise
    '''
    copiedFiles = False
    if labFiles[student] != []:
        copyfile(labFiles[student][0], labFuncsNm)
        copyfile(labFiles[student][1], labTestsNm)
        copiedFiles = True

    return copiedFiles

def runTestsWithPrefix(testFile,prefix,outfile):
    """
    run only tests from testFile with a certain prefix
    Example: runTestsWithPrefix("lab03Tests.py","test_isPrimaryColor")

    see testHelper.py from CS8 lab03 as an example
    """
    loader = unittest.TestLoader()
    loader.testMethodPrefix = prefix

    # open the logfile as the destination of the output
    f = open(outfile, "w")
    suite = loader.discover('.', pattern = testFile) 
    unittest.TextTestRunner(stream=f,verbosity=2).run(suite)
    f.close()

def countTestFailures(filename):
    '''
    Given a file with pyUnit test output, look at the last line to 
    see if the tests passed. 
    If they passed, return 0. Otherwise, return -1
    '''
    f = open(filename, 'r')
    lines = f.readlines()
    lastLine = lines[-1]
    f.close()

    # python ternary operator - woohoo!
    return -1 if "FAIL" in lastLine else 0

def appendHeadText(filename):
    '''
    Append the first few lines of the labFuncsNm and labTestsNm files, respectively,
    to the file given in the 'filename' parameter
    '''
    f = open(filename, 'w')
    f.write("\n############################################\n")
    f.write("beginning of %s:\n", labFuncsNm)

    # call the head command, convert it to a string, and write it to the file
    f.write( str(subprocess.check_output('head -n 5 ' + labFuncsNm, shell=True)) )

    f.write("\n############################################\n")
    f.write("beginning of %s:\n", labTestsNm)

    f.write( str(subprocess.check_output('head -n 5 ' + labTestsNm, shell=True)) )
    f.close()


if __name__ == "__main__":

    findLabFiles()
    allStudents = list(labFiles.keys())
    allStudents.sort()
    sc = open(labDir + "scores.txt", "w")

    sc.write("passed the unit tests: 0\n")
    sc.write("failed some unit test: -1\n")
    sc.write("failed to find lab01Funcs.py or lab01Tests.py: -2\n\n")

    # make a directory for pyUnit output files
    if not os.path.exists(testOutputDir)
        os.makedirs(testOutputDir)

    # basically use the 'touch' command to create files with thse names
    f1 = open(labFuncsNm, "w")
    f2 = open(labTestsNm, "w")
    f1.close()
    f2.close()
    import lab01Tests

    # clean out the current directory to prepare for testing
    cleanFiles()

    # run the tests on all students
    for stud in allStudents:
        status = -2

        # create an output file for the current student
        resultFilePath = testOutputDir + "/" + stud +"_output.txt"
        
        # If the student had files stored in their current dir,
        # then run the tests.
        # If copyfiles returned false, then the student gets a
        # '-2' written to the scores file as a flag that we must  
        # manually check their submission.
        if copyFiles(stud):

            # Change the parameters to runTestsWithPrefix as needed
            runTestsWithPrefix(labTestsNm,"test_milesToKm", resultFilePath)

            # count failures and store in status
            status = countTestFailures(resultFilePath)

            # append 'head' output data to see if student wrote his/her name 
            appendHeadText(resultFilePath)

        cleanFiles()
        sc.write("%s, %d\n" % (stud, status))   

    sc.close()
    print("*** Testing done ***")
