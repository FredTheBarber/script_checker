# script_checker
A python project leveraging openpyxl for running various typographical checks on the contents of excel worksheets and generating an output worksheet with a list of issues to investigate/remediate.

# Prerequisites
You need Python installed, as well as the `openpyxl` library

python: https://www.python.org/downloads/

pip is the Python installer library of choice on most OSes, and is a good way to install openpyxl: https://pypi.org/project/pip/

openpyxl: https://pypi.org/project/openpyxl/


# How to run
First you will need to modify script_checker.py for your scripts' details.
- Place all files to be checked in the `sheets` folder. Note that python has to find these files, so running the program from a different folder will likely result in failure.
- Modify the `JP_COLUMN`, `TL_COLUMN`, `EDIT_COLUMN`, and `QA_COLUMN` variables in `script_checker.py` to point at the correct columns for your worksheet's format
After you have customized these variables for your scripts, run the tool with:

```python script_checker.py```

If everything runs correctly, when it is done, a new file named `errors_and_warnings.xlsx` should have been written in the same folder as script_checker.py, script_checker.py should have only output the following on the console:

```Done.```

# How to modify/extend
Aside from the basic settings in `script_checker.py` which describe the shape of your xlsx files, you may want to modify the checks that are run or implement new ones. These are all implemented in `checks.py` and unit tested in `test_checks.py`.

For each new check you want to implement:
- Add a function in `checks.py`
- Add unit tests for it in `test_checks.py`
- Add the function name to the `CHECKS` variable at the bottom of `checks.py`
And then your check will be run alongside all the others when `script_checker.py` is run.

# How to test
This project has unit tests for each function that implements a check. If you want to run those tests, or add new ones for new checks you implement, you need to install `pytest`: https://pypi.org/project/pytest/

Then, in the same folder as the python files, just run `pytest` from the command prompt. It should generate output like this:
```
C:\script_checker>pytest
================================================= test session starts =================================================
platform win32 -- Python 3.12.6, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\script_checker
collected 9 items

test_checks.py .........                                                                                         [100%]

================================================== 9 passed in 0.04s ==================================================
```
