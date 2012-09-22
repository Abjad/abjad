from abjad import *


def test_iterationtools_iterate_thread_from_component_01():
    '''Iterate only notes.'''

    container = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    container.is_parallel = True
    container[0].name = 'voice 1'
    container[1].name = 'vocie 2'
    staff = Staff(container * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    r'''
    \new Staff {
        <<
            \context Voice = "voice 1" {
                c'8
                d'8
            }
            \context Voice = "vocie 2" {
                e'8
                f'8
            }
        >>
        <<
            \context Voice = "voice 1" {
                g'8
                a'8
            }
            \context Voice = "vocie 2" {
                b'8
                c''8
            }
        >>
    }
    '''

    notes = iterationtools.iterate_thread_from_component(staff.leaves[-1], Note, reverse=True)
    notes = list(notes)

    voice_2_first_half = staff[0][1]
    voice_2_second_half = staff[1][1]

    assert notes[0] is voice_2_second_half[1]
    assert notes[1] is voice_2_second_half[0]
    assert notes[2] is voice_2_first_half[1]
    assert notes[3] is voice_2_first_half[0]


def test_iterationtools_iterate_thread_from_component_02():
    '''Iterate all components.'''

    container = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    container.is_parallel = True
    container[0].name = 'voice 1'
    container[1].name = 'vocie 2'
    staff = Staff(container * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    r'''
    \new Staff {
        <<
            \context Voice = "voice 1" {
                c'8
                d'8
            }
            \context Voice = "vocie 2" {
                e'8
                f'8
            }
        >>
        <<
            \context Voice = "voice 1" {
                g'8
                a'8
            }
            \context Voice = "vocie 2" {
                b'8
                c''8
            }
        >>
    }
    '''

    components = iterationtools.iterate_thread_from_component(staff.leaves[-1], reverse=True)
    components = list(components)

    r'''
    Note(c'', 8)
    Voice{2}
    Note(b', 8)
    Voice{2}
    Note(f', 8)
    Note(e', 8)
    '''

    assert components[0] is staff.leaves[-1]
    assert components[1] is staff[1][1]
    assert components[2] is staff.leaves[-2]
    assert components[3] is staff[0][1]
    assert components[4] is staff[0][1][1]
    assert components[5] is staff[0][1][0]


def test_iterationtools_iterate_thread_from_component_03():

    container = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    container.is_parallel = True
    container[0].name = 'voice 1'
    container[1].name = 'vocie 2'
    staff = Staff(container * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    r'''
    \new Staff {
        <<
            \context Voice = "voice 1" {
                c'8
                d'8
            }
            \context Voice = "vocie 2" {
                e'8
                f'8
            }
        >>
        <<
            \context Voice = "voice 1" {
                g'8
                a'8
            }
            \context Voice = "vocie 2" {
                b'8
                c''8
            }
        >>
    }
    '''

    notes = iterationtools.iterate_thread_from_component(staff.leaves[0], Note)
    notes = list(notes)

    voice_1_first_half = staff[0][0]
    voice_1_second_half = staff[1][0]

    assert notes[0] is voice_1_first_half[0]
    assert notes[1] is voice_1_first_half[1]
    assert notes[2] is voice_1_second_half[0]
    assert notes[3] is voice_1_second_half[1]


def test_iterationtools_iterate_thread_from_component_04():

    container = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    container.is_parallel = True
    container[0].name = 'voice 1'
    container[1].name = 'vocie 2'
    staff = Staff(container * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    r'''
    \new Staff {
        <<
            \context Voice = "voice 1" {
                c'8
                d'8
            }
            \context Voice = "vocie 2" {
                e'8
                f'8
            }
        >>
        <<
            \context Voice = "voice 1" {
                g'8
                a'8
            }
            \context Voice = "vocie 2" {
                b'8
                c''8
            }
        >>
    }
    '''

    components = iterationtools.iterate_thread_from_component(staff.leaves[0])
    components = list(components)

    r'''
    c'8
    Voice{2}
    d'8
    Voice{2}
    g'8
    a'8
    '''

    assert components[0] is staff.leaves[0]
    assert components[1] is staff[0][0]
    assert components[2] is staff.leaves[1]
    assert components[3] is staff[1][0]
    assert components[4] is staff[1][0][0]
    assert components[5] is staff[1][0][1]
