# Kyle's tests for grading lab05

import unittest            
from lab05Funcs import *   

class KyleTests05(unittest.TestCase): 

    # tests for smallestInt

    def test_smallestInt_1(self):
       self.assertEqual(  smallestInt([3.141592]), False )

    def test_smallestInt_2(self):
       self.assertEqual(  smallestInt('Lannister'), False )

    def test_smallestInt_3(self):
       self.assertEqual(  smallestInt([-999,-998,-997,999,1,0,-999,9]), -999 )


    # tests for indexOfSmallestInt

 
    def test_indexOfSmallestInt_1(self):
       self.assertEqual( indexOfSmallestInt([-3.141592]), False )

    def test_indexOfSmallestInt_2(self):
       self.assertEqual( indexOfSmallestInt(True), False )

    def test_indexOfSmallestInt_3(self):
       self.assertEqual( indexOfSmallestInt([300,30,0,390,50,0,1]), 2 )

    def test_indexOfSmallestInt_4(self):
       self.assertEqual( indexOfSmallestInt([1,2,3,4,5]), 0 )


    # tests for longestString

    def test_longestString_1(self):
       self.assertEqual(  longestString([3.141592]),    False)

    def test_longestString_2(self):
       self.assertEqual(  longestString(42), False )

    # test to make sure they are checking the *length* of each string, not just ASCII ordering
    # in this case if they are only doing listOfStrings[i] > longest, then they would get 'wolf'
    def test_longestString_3(self):
       self.assertEqual(  longestString(['aaaaaaaaaa','','university','wolf']), 'aaaaaaaaaa' )


    # tests for indexOfShortestString

    def test_indexOfShortestString_1(self):
       self.assertEqual(  indexOfShortestString([[123,12],[-1,-2,-3],[77]]), False )

    def test_indexOfShortestString_2(self):
       self.assertEqual(  indexOfShortestString(80085), False )

    # test to make sure they are checking the *length* of each string, not just ASCII ordering
    # in this case if they are only doing listOfStrings[i] > indexOfShortest, then they would get 'a'
    def test_indexOfShortestString_3(self):
       self.assertEqual(  indexOfShortestString(['b','red','north','wolf','a']), 0 )

    # End of tests for grading lab05

if __name__ == '__main__':
    unittest.main(exit=False)  

