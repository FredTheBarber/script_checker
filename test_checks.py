from checks import check_initial_capitalization

def test_check_initial_capitalization():
    assert(check_initial_capitalization("This is okay.", "") is None)
    assert(check_initial_capitalization("this isn't.", "") is not None)
    assert(check_initial_capitalization("\"This is okay.", "") is None)
    assert(check_initial_capitalization("\"this isn't.", "") is not None)
    
    # This is something of an edge case, and dubious whether it should even be allowed
    # style-wise, but for now, leaning towards allowing it in the automated checks
    assert(check_initial_capitalization("\"777 this is.", "") is None)
    
from checks import check_adjacent_punctuation

def test_check_adjacent_punctuation():
    assert(check_adjacent_punctuation("This is not okay?!", "") is not None)
    assert(check_adjacent_punctuation("This is okay!", "") is None)
    assert(check_adjacent_punctuation("This is not okay—!", "") is not None)

from checks import check_ending_quotation_mark

def test_check_ending_quotation_mark():
    assert(check_ending_quotation_mark("\"This is okay.\"", "「」") is None)
    assert(check_ending_quotation_mark("This is okay.\"", "」") is None)
    assert(check_ending_quotation_mark("This is okay.", "「") is None)
    assert(check_ending_quotation_mark("\"This is okay.", "「") is None)

    assert(check_ending_quotation_mark("This is not okay.", "」") is not None)
    assert(check_ending_quotation_mark("\"This is not okay.", "「」") is not None)
    
from checks import check_starting_quotation_mark

def test_check_starting_quotation_mark():
    assert(check_starting_quotation_mark("\"This is okay.\"", "「」") is None)
    assert(check_starting_quotation_mark("\"This is okay.", "「」") is None)
    assert(check_starting_quotation_mark("\"This is okay.", "「") is None)
    
    assert(check_starting_quotation_mark("This is not okay.", "「") is not None)
    assert(check_starting_quotation_mark("This is not okay.\"", "「") is not None)
    assert(check_starting_quotation_mark("This is not okay.\"", "「」") is not None)
    
from checks import check_double_spacing

def test_check_double_spacing():
    assert(check_double_spacing("This is okay.", "") is None)
    assert(check_double_spacing("This is  not.", "") is not None)
    assert(check_double_spacing("This is   not either.", "") is not None)
    
from checks import check_no_ending_newline

def test_check_no_ending_newline():
    assert(check_no_ending_newline("This is okay.", "") is None)
    assert(check_no_ending_newline("This isn't.\n", "") is not None)
    assert(check_no_ending_newline("This \n is.", "") is None)
    
from checks import check_banned_characters

def test_check_banned_characters():
    assert(check_banned_characters("This is okay.", "") is None)
    assert(check_banned_characters("This isn’t.", "") is not None)
    
from checks import check_oh_god_not_capitalized

def test_check_oh_god_not_capitalized():
    assert(check_oh_god_not_capitalized("Oh god is okay.", "") is None)
    assert(check_oh_god_not_capitalized("Oh God is not.", "") is not None)
    assert(check_oh_god_not_capitalized("And oh god is okay.", "") is None)
    assert(check_oh_god_not_capitalized("And oh God is not.", "") is not None)
    assert(check_oh_god_not_capitalized("With God is okay.", "") is None)
    
from checks import check_ellipsis_length

def test_check_ellipsis_length():
    assert(check_ellipsis_length("This is okay.", "") is None)
    assert(check_ellipsis_length("This isn't..", "") is not None)
    assert(check_ellipsis_length("This is...", "") is None)
    assert(check_ellipsis_length("This isn't....", "") is not None)
    assert(check_ellipsis_length("This isn't either.....", "") is not None)
    assert(check_ellipsis_length("But this is, even though we would never do it......", "") is None)
    assert(check_ellipsis_length("Eight bad........", "") is not None)
    assert(check_ellipsis_length("........", "") is not None)
    assert(check_ellipsis_length("Nine good.........", "") is None)
    assert(check_ellipsis_length(".........", "") is None)
    assert(check_ellipsis_length("...........", "") is not None)
    assert(check_ellipsis_length("............", "") is None)