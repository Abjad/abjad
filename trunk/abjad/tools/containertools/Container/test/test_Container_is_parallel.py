# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Container_is_parallel_01():
    r'''True when container encloses contents in LilyPond << >> brackets,
        otherwise False.'''

    assert not Container([]).is_parallel
    assert not tuplettools.FixedDurationTuplet(Duration(2, 8), []).is_parallel
    assert not Tuplet(Fraction(2, 3), []).is_parallel
    assert scoretools.GrandStaff([]).is_parallel
    assert not stafftools.make_rhythmic_sketch_staff([]).is_parallel
    assert not stafftools.RhythmicStaff([]).is_parallel
    assert not Measure((4, 8), []).is_parallel
    assert Score([]).is_parallel
    assert not Container([]).is_parallel
    assert not Staff([]).is_parallel
    assert scoretools.StaffGroup([]).is_parallel
    assert not Voice([]).is_parallel


def test_Container_is_parallel_02():
    r'''True when container encloses contents in LilyPond << >> brackets,
        otherwise False.'''

    container = Container([])
    container.is_parallel = True
    assert container.is_parallel


def test_Container_is_parallel_03():
    r'''Container 'parallel' is settable.
    '''

    container = Container([])
    assert not container.is_parallel

    container.is_parallel = True
    assert container.is_parallel


def test_Container_is_parallel_04():
    r'''A parallel container can hold Contexts.
    '''
    container = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(container)
    container.is_parallel = True
    assert testtools.compare(
        container.lilypond_format,
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


# Parallel Errors #

def test_Container_is_parallel_05():
    r'''Parallel containers must contain only Contexts.
    It cannot take leaves.'''

    container = Container(notetools.make_repeated_notes(4))
    py.test.raises(AssertionError, 'container.is_parallel = True')


def test_Container_is_parallel_06():
    r'''Parallel containers must contain only Contexts.
    It cannot take Containers.'''

    container = Container(Container(notetools.make_repeated_notes(4)) * 2)
    py.test.raises(AssertionError, 'container.is_parallel = True')
