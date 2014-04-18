#!/usr/bin/python
# grading script for CS8 lab01, Spring 2014

from glob import glob
from shutil import copyfile
from os import *
from os import remove
import sys, subprocess, time
import imp
import unittest

### Some global variable definitions ### 
labFiles = {}           # dictionary of student names as key and list of file names as value
                        # i.e. {'John Snow': ['fileone.py', 'filetwo.py']}
graderTests = "KyleTests.py"
if len(sys.argv) == 2:
    labDir = sys.argv[1]    # get the name of the lab as an argument, i.e. "lab01"
    labFuncsNm = labDir + "Funcs.py"
    labTestsNm = labDir + "Tests.py"
    testOutputDir = labDir + "TestOutput"

def findLabFiles():
    ''' 
    Iterates through the student name directories and copies the data into the labFiles dictionary
    '''

    # glob returns all pathnames matching the specified pattern
    tmpStudents = glob("%s/*"%(labDir))
    students = []
    for paths in tmpStudents:
        tmp = paths.split('/')
        student = tmp[1]
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
        funcsFile=glob("%s/%s/%s/%s"%(labDir,student, labDir, labFuncsNm))
        testsFile=glob("%s/%s/%s/%s"%(labDir,student, labDir, labTestsNm))

        # if both files do NOT exist in the directory
        if len(funcsFile) == 0 or len(testsFile) == 0:
            fileList += []
            labFiles[student] = fileList
        # else, if both files DO exist in the directory 
        elif len(funcsFile) != 0 and len(testsFile) != 0:
            fileList += funcsFile + testsFile
            labFiles[student] = fileList
        # else, if one of the two is not there (this is a problem)
        else:
            fileList += []
            labFiles[student] = fileList

def cleanFiles():
    '''
    Cleans the lab files if any exist in the current directory 
    '''
    if path.isfile(labFuncsNm):
        remove(labFuncsNm)
    if path.isfile(labTestsNm):
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

def runTestsWithPrefix(testFile1,testFile2,prefix,outfile):
    """
    run tests from testFile1 and testFile2 with a certain prefix, then 
    output the results into outfile.

    see testHelper.py from CS8 lab03 as a basic example
    """
    loader = unittest.TestLoader()
    loader.testMethodPrefix = prefix

    print("*** run test params " + testFile1 + ", " + testFile2 + ", " + outfile)
    # open the outfile as the destination of the output
    f = open(outfile, "w")

    # add all the unit tests into the TestSuite object
    suite = loader.discover('.', pattern = testFile1) 
    suite.addTest( loader.discover('.', pattern = testFile2) )

    # pass the file as the stream location for output
    unittest.TextTestRunner(stream=f,verbosity=2).run(suite)
    f.close()

def countTestFailures(filename):
    '''
    Given a file with pyUnit test output, look at the last line to 
    see if the tests passed, and look and make sure the student added
    enough of their own tests.
    If they passed the tests and had the proper amount, return 0. 
    If the tests failed, return -1
    If they did not have enough tests, return -2
    '''
    f = open(filename, 'r')
    lines = f.readlines()
    lastLine = lines[-1]
    thirdLastLine = lines[-3]
    numtests = thirdLastLine.split()[1]
    f.close()

    if int(numtests) >= 8:
        if "FAIL" in lastLine:
            return -1
        else: 
            return 0
    else:
        return -2

    # python ternary operator - woohoo!
    # return -1 if "FAIL" in lastLine else 0

def appendHeadText(filename):
    '''
    Append the first few lines of the labFuncsNm and labTestsNm files, respectively,
    to the file given in the 'filename' parameter
    '''
    f = open(filename, 'w')
    f.write("\n############################################\n")
    f.write("beginning of %s:\n"%labFuncsNm)

    # call the head command, convert it to a string, and write it to the file
    # needs the decode() because of python2/python3 weirdness with byte arrays and strings
    f.write( subprocess.check_output('head -n 5 ' + labFuncsNm, shell=True).decode("utf-8") )

    f.write("\n############################################\n")
    f.write("beginning of %s:\n"%labTestsNm)

    f.write( subprocess.check_output('head -n 5 ' + labTestsNm, shell=True).decode("utf-8") )
    f.close()

def printHeadText(student):
    '''
    Print the first few lines of the labFuncsNm and labTestsNm files, respectively,
    for the 'student' passed in
    '''
    print("\n-----------------------------------------------\n")
    print("These files belong to " + student + "\n")
    print("beginning of %s:\n" % labFuncsNm)

    # call the head command, convert it to a string
    # needs the decode() because of python2/python3 weirdness with byte arrays and strings
    print( subprocess.check_output('head -n 5 ' + labFuncsNm, shell=True).decode("utf-8") )

    # sleep, to allow myself to record if the student didn't include their name
    time.sleep(3)

    print("\n-----------------------------------------------\n")
    print("beginning of %s:\n" % labTestsNm)
    print( subprocess.check_output('head -n 5 ' + labTestsNm, shell=True).decode("utf-8") )
    time.sleep(3)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 grade_lab01.py <directory of stuff to grade>\n")
    else:
        findLabFiles()
        allStudents = list(labFiles.keys())
        allStudents.sort()
        sc = open("scores.txt", "w")

        sc.write("passed the unit tests: 0\n")
        sc.write("failed some unit test: -1\n")
        sc.write("failed to add enough new tests: -2\n")
        sc.write("failed to find lab01Funcs.py or lab01Tests.py: -3\n\n")

        # make a directory for pyUnit output files (using os.path.exists and os.makedirs)
        if not path.exists(testOutputDir):
            makedirs(testOutputDir)

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
            status = -3

            # create an output file for the current student
            resultFilePath = testOutputDir + "/" + stud +"_output.txt"
            resultFile = open(resultFilePath,'w')
            resultFile.close()
            
            # If the student had files stored in their current dir,
            # then run the tests.
            # If copyfiles returned false, then the student gets a
            # '-3' written to the scores file as a flag that we must  
            # manually check their submission.
            if copyFiles(stud):

                # Change the parameters to runTestsWithPrefix as needed
                runTestsWithPrefix(labTestsNm,graderTests,"test_milesToKm", resultFilePath)

                # count failures and store in status
                status = countTestFailures(resultFilePath)

                # print 'head' output data to see if student wrote his/her name 
                printHeadText(stud)

            cleanFiles()
            sc.write("%s, %d\n" % (stud, status))   

        sc.close()
        print("*** Testing done ***")      
