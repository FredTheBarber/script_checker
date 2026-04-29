from collections.abc import Callable
from functools import wraps

### Don't touch unless you know exactly what you're doing
class Checker:
    __checks = {}

    def _check(self):
        def wrapper(func: Callable[[str, str], None]):
            self.__checks[func.__name__] = func
        return wrapper
    
    def get_check(self, name):
        '''Returns the registered check with a given `name`
        Raises AttributeError if no check was registered with the given name'''

        return self.__checks[name]
    
    def run_checks(self, en, jp):
        '''Runs all registered checks
        Returns a list of all error messages from failed checks'''

        errors = [check(en, jp) for check in self.__checks.values()]
        errors = filter(lambda x: x is not None, errors)
        return errors

##### To implement a check for a row:
##### - Create a new function with the following signature:
##### * @checker._check()
##### * def check_name(en_line: str, jp_line: str):
#####   Where check_name is a unique string identifying your test
##### - Have it return nothing if the check succeeds
#####   and return an error string if the check fails
##### - The error string will be used in the `errors_and_warnings` output sheet
##### - Optionally, implement and run unit tests in `test_checks.py`

def new_checker():
    '''Creates a new Checker instance and populates its internal list of checks'''
    
    checker = Checker()

    @checker._check()
    def banned_characters(en_line: str, jp_line: str):
        banned_characters =[ '’', '‘', '“', '”', '…', '&']
        errors = [f'Banned character: [{char}]' for char in banned_characters if char in en_line]     
        if errors:
            return '\n'.join(errors)

    @checker._check()
    def ending_newline(en_line: str, jp_line: str):
        if en_line.endswith("\n"):
            return "Line ends with \n"

    @checker._check()
    def double_spacing(en_line: str, jp_line: str):
        if "  " in en_line:
            return 'Line contains multiple sequential spaces'

    @checker._check()
    def starting_quotation_mark(en_line: str, jp_line: str):
        if jp_line.startswith("「"):
            if not en_line.startswith("\""):
                return "Mismatched quotes: JP line has 「, EN does not start with \""
        else:
            if en_line.startswith("\""):
                return "Mismatched quotes: JP line does not have 「, EN line starts with \""

    @checker._check()
    def ending_quotation_mark(en_line: str, jp_line: str):
        if jp_line.endswith("」"):
            if not en_line.endswith("\""):
                return "Mismatched quotes: JP line has 」, EN does not end with \""
        else:
            if en_line.endswith("\""):
                return "Mismatched quotes: JP line does not have 」, EN line ends with \""

    @checker._check()
    def adjacent_punctuation(en_line: str, jp_line: str):
        punctuation = ",.;:—?!"
        for punc in punctuation:
            start = -1
            while (start := en_line.find(punc, start+1)) != -1:
                if start >= len(en_line) - 1:
                    return
                if en_line[start+1] in punctuation and (en_line[start] != en_line[start + 1] or en_line[start] != '.'):
                    return "Adjacent punctuation found"
        
    ### Because of the way the script is formatted, with a single game line
    ### split across multiple spreadsheet rows, this check is too noisy
    ### It also probably needs a smarter implementation, tbh
    # @checker._check()
    # def initial_capitalization(en_line: str, jp_line: str):
    #     for character in en_line:
    #         if character.isalpha():
    #             if character.capitalize() == character:
    #                 return
    #             else:
    #                 return "First letter is not capitalized"
    #         if character.isnumeric():
    #             return

    @checker._check()
    def oh_god_not_capitalized(en_line: str, jp_line: str):
        if "oh God" in en_line or "Oh God" in en_line:
            return "Don't capitalize 'god' in 'Oh god'"

    @checker._check()
    def ellipsis_length(en_line: str, jp_line: str):
        last_location = len(en_line) - 1
        start = 0
        while True:
            period_location = en_line.find(".", start)
            if period_location == -1 or period_location == last_location:
                return

            if en_line[period_location + 1] != ".":
                start = period_location + 1
                continue
            
            count = 1
            
            while en_line[period_location + 1] == '.':
                period_location += 1
                count += 1
                if period_location == last_location:
                    if count % 3 != 0:
                        return "Ellipsis length = " + str(count)
                    return

            if count % 3 != 0:
                return "Ellipsis length = " + str(count)

            start = period_location + 1

    return checker