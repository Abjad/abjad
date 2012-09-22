from abjad import *
import py.test


def test_iterationtools_iterate_namesakes_from_component_01():

    container = Container(Staff(notetools.make_repeated_notes(2)) * 2)
    container.is_parallel = True
    container[0].name = 'staff 1'
    container[1].name = 'staff 2'
    score = Score([])
    score.is_parallel = False
    score.extend(container * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(score)

    r'''

    \new Score {
        <<
            \context Staff = "staff 1" {
                c'8
                d'8
            }
            \context Staff = "staff 2" {
                e'8
                f'8
            }
        >>
        <<
            \context Staff = "staff 1" {
                g'8
                a'8
            }
            \context Staff = "staff 2" {
                b'8
                c''8
            }
        >>
    }
    '''

    staves = iterationtools.iterate_namesakes_from_component(score[1][0], reverse=True)
    staves = list(staves)

    assert staves[0] is score[1][0]
    assert staves[0].name == 'staff 1'

    assert staves[1] is score[0][0]
    assert staves[1].name == 'staff 1'


def test_iterationtools_iterate_namesakes_from_component_02():

    container = Container(Staff(notetools.make_repeated_notes(2)) * 2)
    container.is_parallel = True
    container[0].name = 'staff 1'
    container[1].name = 'staff 2'
    score = Score([])
    score.is_parallel = False
    score.extend(container * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(score)

    r'''

    \new Score {
        <<
            \context Staff = "staff 1" {
                c'8
                d'8
            }
            \context Staff = "staff 2" {
                e'8
                f'8
            }
        >>
        <<
            \context Staff = "staff 1" {
                g'8
                a'8
            }
            \context Staff = "staff 2" {
                b'8
                c''8
            }
        >>
    }
    '''

    notes = iterationtools.iterate_namesakes_from_component(score.leaves[-1], reverse=True)
    notes = list(notes)

    r'''
    Note(c'', 8)
    Note(b', 8)
    Note(f', 8)
    Note(e', 8)
    '''

    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        notes[0], Staff).name == 'staff 2'
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        notes[1], Staff).name == 'staff 2'
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        notes[2], Staff).name == 'staff 2'
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        notes[3], Staff).name == 'staff 2'


def test_iterationtools_iterate_namesakes_from_component_03():
    '''Optional start and stop keywords.'''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    g = iterationtools.iterate_namesakes_from_component(
        t.leaves[-2], reverse=True, start=0, stop=3)

    assert g.next() is t.leaves[-2]
    assert g.next() is t.leaves[-3]
    assert g.next() is t.leaves[-4]
    assert py.test.raises(StopIteration, 'g.next()')


def test_iterationtools_iterate_namesakes_from_component_04():
    '''Optional start and stop keywords.'''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    g = iterationtools.iterate_namesakes_from_component(
        t.leaves[-2], reverse=True, start=2)

    assert g.next() is t.leaves[-4]
    assert g.next() is t.leaves[-5]
    assert g.next() is t.leaves[-6]
    assert py.test.raises(StopIteration, 'g.next()')


def test_iterationtools_iterate_namesakes_from_component_05():

    container = Container(Staff(notetools.make_repeated_notes(2)) * 2)
    container.is_parallel = True
    container[0].name = 'staff 1'
    container[1].name = 'staff 2'
    score = Score([])
    score.is_parallel = False
    score.extend(container * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(score)

    r'''

    \new Score {
        <<
            \context Staff = "staff 1" {
                c'8
                d'8
            }
            \context Staff = "staff 2" {
                e'8
                f'8
            }
        >>
        <<
            \context Staff = "staff 1" {
                g'8
                a'8
            }
            \context Staff = "staff 2" {
                b'8
                c''8
            }
        >>
    }
    '''

    staves = iterationtools.iterate_namesakes_from_component(score[0][0])
    staves = list(staves)

    assert staves[0] is score[0][0]
    assert staves[0].name == 'staff 1'

    assert staves[1] is score[1][0]
    assert staves[1].name == 'staff 1'


def test_iterationtools_iterate_namesakes_from_component_06():

    container = Container(Staff(notetools.make_repeated_notes(2)) * 2)
    container.is_parallel = True
    container[0].name = 'staff 1'
    container[1].name = 'staff 2'
    score = Score([])
    score.is_parallel = False
    score.extend(container * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(score)

    r'''

    \new Score {
        <<
            \context Staff = "staff 1" {
                c'8
                d'8
            }
            \context Staff = "staff 2" {
                e'8
                f'8
            }
        >>
        <<
            \context Staff = "staff 1" {
                g'8
                a'8
            }
            \context Staff = "staff 2" {
                b'8
                c''8
            }
        >>
    }
    '''

    notes = iterationtools.iterate_namesakes_from_component(score.leaves[0])
    notes = list(notes)

    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        notes[0], Staff).name == 'staff 1'
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        notes[1], Staff).name == 'staff 1'
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        notes[2], Staff).name == 'staff 1'
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        notes[3], Staff).name == 'staff 1'


def test_iterationtools_iterate_namesakes_from_component_07():
    '''Optional start and stop keywords.'''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    g = iterationtools.iterate_namesakes_from_component(t.leaves[1], start=0, stop=3)

    assert g.next() is t.leaves[1]
    assert g.next() is t.leaves[2]
    assert g.next() is t.leaves[3]
    assert py.test.raises(StopIteration, 'g.next()')


def test_iterationtools_iterate_namesakes_from_component_08():
    '''Optional start and stop keywords.'''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    g = iterationtools.iterate_namesakes_from_component(t.leaves[1], start=2)

    assert g.next() is t.leaves[3]
    assert g.next() is t.leaves[4]
    assert g.next() is t.leaves[5]
    assert py.test.raises(StopIteration, 'g.next()')
