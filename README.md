# grading_scripts

for TA work

### cs8s14 labs
The files that I used to grade each lab will be in a unique directory. These are intended to be used after the code has been extracted from the `TURNIN` directory of the class account. The typical usage is 

```python3 grade_labXX.py <directory of stuff to grade>```

Where the directory of stuff to grade will be `labXX/` containing each student's code in named dirctories. As the script processes the students' code, output will be put into a `labXXTestOutput/` folder with an individual output file for each student. 
Thus, it will be filled with files named `<student>_output.txt`, and each of these files will contain the unittest output from the tests that were executed on that student's code. Lastly, in the main directory where the script is run, there will be a file called `scores.txt` containing a status code for each student. The status codes indicate if all tests passed, if there were errors, if they were missing code, etc.

### turnin
This directory contains a script which extracts code from the `TURNIN` directory (on the class account) into a work directory. See
`turnin/INSTRUCTIONS` for how to use this script.
