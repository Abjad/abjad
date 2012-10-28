from abjad import *
import py.test


def test_Staff_time_signature_01():
    '''Force time_signature on nonempty staff.'''

    t = Staff(Note("c'4") * 8)
    contexttools.TimeSignatureMark((2, 4))(t)
    assert t.lilypond_format == "\\new Staff {\n\t\\time 2/4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"
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


def test_Staff_time_signature_02():
    '''Force time_signature on empty staff.'''

    t = Staff([])
    contexttools.TimeSignatureMark((2, 4))(t)

    r'''
    \new Staff {
        \time 2/4
    }
    '''

    assert t.lilypond_format == '\\new Staff {\n\t\\time 2/4\n}'


def test_Staff_time_signature_03():
    '''Staff time_signature carries over to staff-contained leaves.'''

    t = Staff(Note("c'4") * 8)
    contexttools.TimeSignatureMark((2, 4))(t)
    for x in t:
        assert contexttools.get_effective_time_signature(x) == contexttools.TimeSignatureMark((2, 4))


def test_Staff_time_signature_04():
    '''Staff time_signature set and then clear.
    '''

    t = Staff(Note("c'4") * 8)
    contexttools.TimeSignatureMark((2, 4))(t)
    contexttools.get_effective_time_signature(t).detach()
    for leaf in t:
        assert contexttools.get_effective_time_signature(leaf) is None
