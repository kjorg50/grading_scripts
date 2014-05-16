# testHelper.py

# If you have a file like lab01Tests.py or lab04Tests.py with
# so many tests that it gets confusing, this file can help you 
# focus on just one function at a time.

# See the comments at the bottom.

import unittest

logfile = "log.txt"

def runTestsWithPrefix(testFile,testFile2,prefix):
    """
    run only tests from testFile with a certain prefix
    Example: runTestsWithPrefix("lab03Tests.py","test_isPrimaryColor")
    """
    loader = unittest.TestLoader()
    loader.testMethodPrefix = prefix
    f = open(logfile, 'w')
    suite = loader.discover('.', pattern = testFile)
    print("Cases %d" % (suite.countTestCases()))
    suite.addTest(loader.discover('.', pattern = testFile2))
    print("Cases %d" % (suite.countTestCases()))
    
    unittest.TextTestRunner(stream=f,verbosity=2).run(suite)
    f.close()

if __name__ == "__main__":

    # Change the parameters to runTestsWithPrefix as needed
    runTestsWithPrefix("lab01Tests.py","KyleTests.py","test_milesToKm")
