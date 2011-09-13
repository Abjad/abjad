from abjad import *
import py.test


def test_contexttools_get_effective_tempo_01():
    '''Tempo interface works on staves.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    contexttools.TempoMark(Duration(1, 8), 38, target_context = Staff)(t)
    contexttools.TempoMark(Duration(1, 8), 42, target_context = Staff)(t[2])

    r'''
    \new Staff {
        \tempo 8=38
        c'8
        d'8
        \tempo 8=42
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert contexttools.get_effective_tempo(t[0]) == contexttools.TempoMark(Duration(1, 8), 38)
    assert contexttools.get_effective_tempo(t[1]) == contexttools.TempoMark(Duration(1, 8), 38)
    assert contexttools.get_effective_tempo(t[2]) == contexttools.TempoMark(Duration(1, 8), 42)
    assert contexttools.get_effective_tempo(t[3]) == contexttools.TempoMark(Duration(1, 8), 42)
    assert t.format == "\\new Staff {\n\t\\tempo 8=38\n\tc'8\n\td'8\n\t\\tempo 8=42\n\te'8\n\tf'8\n}"



def test_contexttools_get_effective_tempo_02():
    '''Tempo interface works on chords.
    '''

    t = Staff([Chord([2, 3, 4], (1, 4))])
    contexttools.TempoMark(Duration(1, 8), 38, target_context = Staff)(t[0])

    r'''
    \new Staff {
        \tempo 8=38
        <d' ef' e'>4
    }
    '''

    assert t.format == "\\new Staff {\n\t\\tempo 8=38\n\t<d' ef' e'>4\n}"


def test_contexttools_get_effective_tempo_03():
    '''Tempo interface accepts durations.'''

    staff = Staff([Note("c'4")])
    contexttools.TempoMark(Duration(1, 8), 38, target_context = Staff)(staff[0])

    r'''
    \new Staff {
        \tempo 8=38
        c'4
    }
    '''

    assert staff.format == "\\new Staff {\n\t\\tempo 8=38\n\tc'4\n}"


def test_contexttools_get_effective_tempo_04():
    '''Detach tempo mark.
    '''

    staff = Staff([Note("c'4")])
    tempo = contexttools.TempoMark(Duration(1, 8), 38, target_context = Staff)(staff[0])
    tempo.detach()


    r'''
    \new Staff {
        c'4
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'4\n}"
