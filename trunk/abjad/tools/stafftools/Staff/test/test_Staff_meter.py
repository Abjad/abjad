from abjad import *
import py.test


def test_Staff_meter_01():
    '''Force meter on nonempty staff.'''

    t = Staff(Note("c'4") * 8)
    contexttools.TimeSignatureMark((2, 4))(t)
    assert t.format == "\\new Staff {\n\t\\time 2/4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"
    r'''
    \new Staff {
        \time 2/4
        c'4
        c'4
        c'4
        c'4
        c'4
        c'4
        c'4
        c'4
    }
    '''


def test_Staff_meter_02():
    '''Force meter on empty staff.'''

    t = Staff([])
    contexttools.TimeSignatureMark((2, 4))(t)

    r'''
    \new Staff {
        \time 2/4
    }
    '''

    assert t.format == '\\new Staff {\n\t\\time 2/4\n}'


def test_Staff_meter_03():
    '''Staff meter carries over to staff-contained leaves.'''

    t = Staff(Note("c'4") * 8)
    contexttools.TimeSignatureMark((2, 4))(t)
    for x in t:
        assert contexttools.get_effective_time_signature(x) == contexttools.TimeSignatureMark((2, 4))


def test_Staff_meter_04():
    '''Staff meter set and then clear.
    '''

    t = Staff(Note("c'4") * 8)
    contexttools.TimeSignatureMark((2, 4))(t)
    contexttools.get_effective_time_signature(t).detach()
    for leaf in t:
        assert contexttools.get_effective_time_signature(leaf) is None
