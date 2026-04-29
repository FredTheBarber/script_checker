from checks import new_checker

checker = new_checker()

##### To implement a new test:
##### - Create a new function with the following signature:
##### * def test_name():
##### *     check = checker.get_check('name')
#####   where `name` is the exact name of the check you wish to test
##### - Implement assertions following the existing examples, where `is None` indicates success, and `is not None` indicates a failed check 

def test_adjacent_punctuation():
    check = checker.get_check('adjacent_punctuation')
    
    assert(check("This is not okay?!", "") is not None)
    assert(check("This is okay!", "") is None)
    assert(check("This is not okay—!", "") is not None)

def test_ending_quotation_mark():
    check = checker.get_check('ending_quotation_mark')
    
    assert(check("\"This is okay.\"", "「」") is None)
    assert(check("This is okay.\"", "」") is None)
    assert(check("This is okay.", "「") is None)
    assert(check("\"This is okay.", "「") is None)

    assert(check("This is not okay.", "」") is not None)
    assert(check("\"This is not okay.", "「」") is not None)
    
def test_starting_quotation_mark():
    check = checker.get_check('starting_quotation_mark')

    assert(check("\"This is okay.\"", "「」") is None)
    assert(check("\"This is okay.", "「」") is None)
    assert(check("\"This is okay.", "「") is None)
    
    assert(check("This is not okay.", "「") is not None)
    assert(check("This is not okay.\"", "「") is not None)
    assert(check("This is not okay.\"", "「」") is not None)
    
def test_double_spacing():
    check = checker.get_check('double_spacing')
    
    assert(check("This is okay.", "") is None)
    assert(check("This is  not.", "") is not None)
    assert(check("This is   not either.", "") is not None)
    
def test_ending_newline():
    check = checker.get_check('ending_newline')

    assert(check("This is okay.", "") is None)
    assert(check("This isn't.\n", "") is not None)
    assert(check("This \n is.", "") is None)
    
def test_banned_characters():
    check = checker.get_check('banned_characters')

    assert(check("This is okay.", "") is None)
    assert(check("This isn’t.", "") is not None)
    
def test_oh_god_not_capitalized():
    check = checker.get_check('oh_god_not_capitalized')

    assert(check("Oh god is okay.", "") is None)
    assert(check("Oh God is not.", "") is not None)
    assert(check("And oh god is okay.", "") is None)
    assert(check("And oh God is not.", "") is not None)
    assert(check("With God is okay.", "") is None)
    
def test_ellipsis_length():
    check = checker.get_check('ellipsis_length')

    assert(check("This is okay.", "") is None)
    assert(check("This isn't..", "") is not None)
    assert(check("This is...", "") is None)
    assert(check("This isn't....", "") is not None)
    assert(check("This isn't either.....", "") is not None)
    assert(check("But this is, even though we would never do it......", "") is None)
    assert(check("Eight bad........", "") is not None)
    assert(check("........", "") is not None)
    assert(check("Nine good.........", "") is None)
    assert(check(".........", "") is None)
    assert(check("...........", "") is not None)
    assert(check("............", "") is None)

# def test_check_initial_capitalization():
#     check = checker.get_check('initial_capitalization')

#     assert(check("This is okay.", "") is None)
#     assert(check("this isn't.", "") is not None)
#     assert(check("\"This is okay.", "") is None)
#     assert(check("\"this isn't.", "") is not None)
   
#     # This is something of an edge case, and dubious whether it should even be allowed
#     # style-wise, but for now, leaning towards allowing it in the automated checks
#     assert(check("\"777 this is.", "") is None)