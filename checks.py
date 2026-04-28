##### To implement a check for a row:
##### - make a new function with the same signature as the other checks:
#####   def check_whatever(en_line, jp_line):
##### - have it return nothing if the check succeeds,
#####   and return an error string for the output sheet if the check fails
##### - Add it to the CHECKS array in the check_line() function up above
##### - Implement a test for it in test_checks.py, and be sure to run the tests

def check_banned_characters(en_line, jp_line):
    banned_characters = ['’', '‘', '“', '”', '…', '&']
    error = ""
    for banned_character in banned_characters:
        if banned_character in en_line:
            error += "Banned character " + banned_character + ".\n"
    
    if error != "":
        return error

def check_no_ending_newline(en_line, jp_line):
    banned_terminal_string = "\n"
    if en_line.endswith(banned_terminal_string):
        return "Line ends with " + banned_terminal_string

def check_double_spacing(en_line, jp_line):
    if "  " in en_line:
        return "Line contains multiple sequential spaces"

def check_starting_quotation_mark(en_line, jp_line):
    if jp_line.startswith("「"):
        if en_line.startswith("\""):
            return
        else:
            return "Mismatched quotes: JP line has 「, EN does not start with \""
    else:
        if en_line.startswith("\""):
            return "Mismatched quotes: JP line does not have 「, EN line starts with \""

def check_ending_quotation_mark(en_line, jp_line):
    if jp_line.endswith("」"):
        if en_line.endswith("\""):
            return
        else:
            return "Mismatched quotes: JP line has 」, EN does not end with \""
    else:
        if en_line.endswith("\""):
            return "Mismatched quotes: JP line does not have 」, EN line ends with \""

def check_adjacent_punctuation(en_line, jp_line):
    punctuation = ",.;:—?!"
    for punc in punctuation:
        start = 0
        while True:
            start = en_line.find(punc, start)
            if start == -1:
                break
            if start >= len(en_line) - 1:
                return
            if en_line[start+1] in punctuation and (en_line[start] != en_line[start + 1] or en_line[start] != '.'):
                return "Adjacent punctuation found"
            start += 1
    
    return

def check_initial_capitalization(en_line, jp_line):
    for character in en_line:
        if character.isalpha():
            if character.capitalize() == character:
                return
            else:
                return "First letter is not capitalized"
        if character.isnumeric():
            return

def check_oh_god_not_capitalized(en_line, jp_line):
    if "oh God" in en_line or "Oh God" in en_line:
        return "Don't capitalize 'god' in 'Oh god'"

def check_ellipsis_length(en_line, jp_line):
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


CHECKS = [check_banned_characters, 
          check_no_ending_newline, 
          check_double_spacing, 
          check_starting_quotation_mark, 
          check_ending_quotation_mark,
          check_adjacent_punctuation,
          check_oh_god_not_capitalized,
          check_ellipsis_length,
          ]

### Because of the way the script is formatted, with a single game line
### split across multiple spreadsheet rows, this check is too noisy
### It also probably needs a smarter implementation, tbh
TOO_NOISY_CHECKS = [check_initial_capitalization]