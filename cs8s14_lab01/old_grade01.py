from glob import glob
from shutil import copyfile
from os import remove
from os.path import isfile
import sys
import imp
import math

### Some global variables ### 
labFiles = {}			# dictionary of student names as keys and file names as values
labDir = sys.argv[1]	# get the name of the lab as an argument, i.e. "lab01"
labFileNm = "someFunctions.py"
testData = [ (1, 1.60934), (2, 3.21869), (3, 4.82803), \
(-3, -4.82803) ]

def findLabFiles():
	''' iterates through the student name directories and copies the data into a dict '''

	# glob returns all pathnames matching the specified pattern
	tmpStudents = glob("%s/*"%(labDir))
	students = []
	for student in tmpStudents:
		# do some sanity checks
		if student[0] != '_' and '.' not in student:
			# add the directories with student names into a list
			students = students + [student]

	# this loop goes through and adds each filename to the associated student
	# name in the dictionary
	for student in students:
		# add each students name as a key in a dictionary
		labFiles[student] = {}

		# look for the files in the main directory
		labFile=glob("%s/%s"%(student, labFileNm))

		if len(labFile) == 0:
			# If they weren't there, check if the student turned in the 
			# files in a lab directory
			labFile=glob("%s/%s/%s"%(student, labDir, labFileNm))
			if len(labFile) == 0:
				labFiles[student] = ""
			else:
				labFiles[student] = labFile[0]
		else:
			labFiles[student] = labFile[0]


def copyFiles(student):
	copiedFiles = False
	if labFiles[student] != "":
		copyfile(labFiles[student], labFileNm)
		copiedFiles = True

	return copiedFiles

def cleanFiles():
	if isfile(labFileNm):
		remove(labFileNm)

def testLab(student):
	'''
	Runs the tests for the current lab. Returns the number of tests passed. 
	If there is an error running the tests, return -1
	'''
	passed = 0


	if isfile(labFileNm):
		try:
			# use imp to reload the module for each students' code
			imp.reload(someFunctions)
		except Exception as inst:
			print(inst)
			return -1 

	for i in range(0, 4):
		try:
			kms = 0
			kms = someFunctions.milesToKm(testData[i][0])
		except Exception as inst:
			print(inst)
			return -1
		if math.fabs(kms - testData[i][1]) < 0.01:
			passed += 1

	return passed

if __name__ == "__main__":
	findLabFiles()
	allStudents = list(labFiles.keys())
	allStudents.sort()
	scores = {}
	sc = open("scores.txt", "w")

	# some items from the grading rubric
	sc.write("failed to call milesToKm(): -1\n")
	sc.write("failed to find someFunctions.py: -2\n\n")

	f = open(labFileNm, "w")
	f.close()
	import someFunctions 

	# clean out the current directory to prepare for testing
	cleanFiles()

	for stud in allStudents:
		results = -2

		# If the student had files stored in their current dir,
		# then run the tests.
		# If copyfiles returned false, then the student gets a
		# '-2' written to the scores file as a flag that we must  
		# manually check their submission.
		if copyFiles(stud):
			results = testLab(stud)

		cleanFiles()
		sc.write("%s, %d\n" % (stud, results))

	sc.close()
	print("*** Testing done ***")
