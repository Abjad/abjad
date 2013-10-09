# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Container_is_simultaneous_01():
    r'''True when container encloses contents in LilyPond << >> brackets,
        otherwise False.'''

    assert not Container([]).is_simultaneous
    assert not tuplettools.FixedDurationTuplet(Duration(2, 8), []).is_simultaneous
    assert not Tuplet(Fraction(2, 3), []).is_simultaneous
    assert scoretools.GrandStaff([]).is_simultaneous
    assert not stafftools.make_rhythmic_sketch_staff([]).is_simultaneous
    assert not stafftools.RhythmicStaff([]).is_simultaneous
    assert not Measure((4, 8), []).is_simultaneous
    assert Score([]).is_simultaneous
    assert not Container([]).is_simultaneous
    assert not Staff([]).is_simultaneous
    assert scoretools.StaffGroup([]).is_simultaneous
    assert not Voice([]).is_simultaneous


def test_Container_is_simultaneous_02():
    r'''True when container encloses contents in LilyPond << >> brackets,
        otherwise False.'''

    container = Container([])
    container.is_simultaneous = True
    assert container.is_simultaneous


def test_Container_is_simultaneous_03():
    r'''Container 'simultaneous' is settable.
    '''

    container = Container([])
    assert not container.is_simultaneous

    container.is_simultaneous = True
    assert container.is_simultaneous


def test_Container_is_simultaneous_04():
    r'''A simultaneous container can hold Contexts.
    '''
    container = Container([Voice("c'8 cs'8"), Voice("d'8 ef'8")])
    container.is_simultaneous = True
    assert testtools.compare(
        container,
        r'''
        <<
            \new Voice {
                c'8
                cs'8
            }
            \new Voice {
                d'8
                ef'8
            }
        >>
        '''
        )

    r'''
    <<
        \new Voice {
            c'8
            cs'8
        }
        \new Voice {
            d'8
            ef'8
        }
    >>
    '''


# simultaneous Errors #

def test_Container_is_simultaneous_05():
    r'''simultaneous containers must contain only Contexts.
    It cannot take leaves.'''

    container = Container(notetools.make_repeated_notes(4))
    py.test.raises(AssertionError, 'container.is_simultaneous = True')


def test_Container_is_simultaneous_06():
    r'''simultaneous containers must contain only Contexts.
    It cannot take Containers.'''

    container = Container(Container(notetools.make_repeated_notes(4)) * 2)
    py.test.raises(AssertionError, 'container.is_simultaneous = True')
