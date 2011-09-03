from abjad import *


def test_SchemeNumber___init___01():

    t = Staff([])
    t.override.staff_symbol.thickness = schemetools.SchemeNumber(4)

    r'''
    \new Staff \with {
        \override StaffSymbol #'thickness = #4
    } {
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override StaffSymbol #'thickness = #4\n} {\n}"
