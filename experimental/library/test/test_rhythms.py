from abjad import *
from experimental import library


def test_rhythms_01():
    '''Sixteenths.
    '''

    leaf_lists = library.sixteenths([(4, 8), (3, 8)])
    containers = [Container(x) for x in leaf_lists]
    staff = Staff(containers)

    r'''
    \new Staff {
        {
            c'16
            c'16
            c'16
            c'16
            c'16
            c'16
            c'16
            c'16
        }
        {
            c'16
            c'16
            c'16
            c'16
            c'16
            c'16
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t}\n\t{\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t}\n}"


def test_rhythms_02():
    '''Eighths.
    '''

    leaf_lists = library.eighths([(4, 8), (3, 8)])
    containers = [Container(x) for x in leaf_lists]
    staff = Staff(containers)

    r'''
    \new Staff {
        {
            c'8
            c'8
            c'8
            c'8
        }
        {
            c'8
            c'8
            c'8
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\t{\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n}"


def test_rhythms_03():
    '''Quarters.
    '''

    leaf_lists = library.quarters([(4, 8), (3, 8)])
    containers = [Container(x) for x in leaf_lists]
    staff = Staff(containers)

    r'''
    \new Staff {
        {
            c'4
            c'4
        }
        {
            c'4
            c'8
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\tc'4\n\t\tc'4\n\t}\n\t{\n\t\tc'4\n\t\tc'8\n\t}\n}"


def test_rhythms_04():
    '''Thirty-seconds.
    '''

    leaf_lists = library.thirty_seconds([(4, 8), (3, 8)])
    containers = [Container(x) for x in leaf_lists]
    staff = Staff(containers)

    r'''
    \new Staff {
        {
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
        }
        {
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
            c'32
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t}\n\t{\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t\tc'32\n\t}\n}"
