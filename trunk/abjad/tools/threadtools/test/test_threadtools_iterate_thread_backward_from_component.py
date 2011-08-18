from abjad import *
from abjad.tools import threadtools


def test_threadtools_iterate_thread_backward_from_component_01():
    '''Iterate only notes.'''

    container = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    container.is_parallel = True
    container[0].name = 'voice 1'
    container[1].name = 'vocie 2'
    staff = Staff(container * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)

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

    notes = threadtools.iterate_thread_backward_from_component(staff.leaves[-1], Note)
    notes = list(notes)

    voice_2_first_half = staff[0][1]
    voice_2_second_half = staff[1][1]

    assert notes[0] is voice_2_second_half[1]
    assert notes[1] is voice_2_second_half[0]
    assert notes[2] is voice_2_first_half[1]
    assert notes[3] is voice_2_first_half[0]


def test_threadtools_iterate_thread_backward_from_component_02():
    '''Iterate all components.'''

    container = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    container.is_parallel = True
    container[0].name = 'voice 1'
    container[1].name = 'vocie 2'
    staff = Staff(container * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)

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

    components = threadtools.iterate_thread_backward_from_component(staff.leaves[-1])
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
