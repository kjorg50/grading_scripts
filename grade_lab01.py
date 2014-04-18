# grading script for CS8 lab01, Spring 2014

from glob import glob
from shutil import copyfile
from os import remove
from os.path import isfile
import sys
import imp
import unittest

### Some global variable definitions ### 
logFile = 'logfile.txt'
labFiles = {}           # dictionary of student names as key and list of file names as value
                        # i.e. {'John Snow': ['fileone.py', 'filetwo.py']}
labDir = sys.argv[1]    # get the name of the lab as an argument, i.e. "lab01"
labFuncsNm = labDir + "Funcs.py"
labTestsNm = labDir + "Tests.py"

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

    # python ternary operator - woohoo!
    return -1 if "FAIL" in lastLine else 0

if __name__ == "__main__":

    findLabFiles()
    allStudents = list(labFiles.keys())
    allStudents.sort()
    sc = open("scores.txt", "w")

    sc.write("failed some unit test: -1\n")
    sc.write("failed to find lab01Funcs.py or lab01Tests.py: -2\n\n")

    # TODO - make a directory for pyUnit output files

    # basically use the 'touch' command to create files with thse names
    f1 = open(labFuncsNm, "w")
    f2 = open(labTestsNm, "w")
    f1.close()
    f2.close()
    import lab01Tests

    for stud in allStudents:
        results = -2

        # TODO - create an output file for the current student

        

        # If the student had files stored in their current dir,
        # then run the tests.
        # If copyfiles returned false, then the student gets a
        # '-2' written to the scores file as a flag that we must  
        # manually check their submission.
        if copyFiles(stud):

            # TODO - run unit tests and output to specific student file in the special directory
            # TODO - count failures and store in results
            results = countTestFailures()

        cleanFiles()
        sc.write("%s, %d\n" % (stud, results))

    # Change the parameters to runTestsWithPrefix as needed
    runTestsWithPrefix("lab01Tests.py","test_milesToKm")
