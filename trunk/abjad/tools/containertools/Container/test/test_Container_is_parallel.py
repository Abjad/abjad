from abjad import *
import py.test


def test_Container_is_parallel_01():
    '''True when container encloses contents in LilyPond << >> brackets,
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
    '''True when container encloses contents in LilyPond << >> brackets,
        otherwise False.'''

    t = Container([])
    t.is_parallel = True
    assert t.is_parallel


def test_Container_is_parallel_03():
    '''Container 'parallel' is settable.'''

    t = Container([])
    assert not t.is_parallel

    t.is_parallel = True
    assert t.is_parallel


def test_Container_is_parallel_04():
    '''A parallel container can hold Contexts.'''
    t = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    t.is_parallel = True
    assert t.format == "<<\n\t\\new Voice {\n\t\tc'8\n\t\tcs'8\n\t}\n\t\\new Voice {\n\t\td'8\n\t\tef'8\n\t}\n>>"

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
    '''Parallel containers must contain only Contexts.
    It cannot take leaves.'''

    t = Container(notetools.make_repeated_notes(4))
    py.test.raises(AssertionError, 't.is_parallel = True')


def test_Container_is_parallel_06():
    '''Parallel containers must contain only Contexts.
    It cannot take Containers.'''

    t = Container(Container(notetools.make_repeated_notes(4)) * 2)
    py.test.raises(AssertionError, 't.is_parallel = True')
