from abjad import *


def test_ClefMark___copy___01():
    '''Clef marks copy.
    '''

    t = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    contexttools.ClefMark('treble')(t[0])
    contexttools.ClefMark('bass')(t[4])
    t.extend(componenttools.copy_components_and_immediate_parent_of_first_component(t[:2]))

    r'''
    \new Staff {
        \clef "treble"
        c'8
        cs'8
        d'8
        ef'8
        \clef "bass"
        e'8
        f'8
        fs'8
        g'8
        \clef "treble"
        c'8
        cs'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert contexttools.get_effective_clef(t[0]) == contexttools.ClefMark('treble')
    assert contexttools.get_effective_clef(t[1]) == contexttools.ClefMark('treble')
    assert contexttools.get_effective_clef(t[2]) == contexttools.ClefMark('treble')
    assert contexttools.get_effective_clef(t[3]) == contexttools.ClefMark('treble')
    assert contexttools.get_effective_clef(t[4]) == contexttools.ClefMark('bass')
    assert contexttools.get_effective_clef(t[5]) == contexttools.ClefMark('bass')
    assert contexttools.get_effective_clef(t[6]) == contexttools.ClefMark('bass')
    assert contexttools.get_effective_clef(t[7]) == contexttools.ClefMark('bass')
    assert contexttools.get_effective_clef(t[8]) == contexttools.ClefMark('treble')
    assert contexttools.get_effective_clef(t[9]) == contexttools.ClefMark('treble')

    assert t.format == '''\\new Staff {\n\t\\clef "treble"\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef "bass"\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\t\\clef "treble"\n\tc'8\n\tcs'8\n}'''


def test_ClefMark___copy___02():
    '''Implicit clefs do not copy.
    '''

    t = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    contexttools.ClefMark('treble')(t[0])
    contexttools.ClefMark('bass')(t[4])
    t.extend(componenttools.copy_components_and_immediate_parent_of_first_component(t[2:4]))

    assert componenttools.is_well_formed_component(t)
    assert contexttools.get_effective_clef(t[0]) == contexttools.ClefMark('treble')
    assert contexttools.get_effective_clef(t[1]) == contexttools.ClefMark('treble')
    assert contexttools.get_effective_clef(t[2]) == contexttools.ClefMark('treble')
    assert contexttools.get_effective_clef(t[3]) == contexttools.ClefMark('treble')
    assert contexttools.get_effective_clef(t[4]) == contexttools.ClefMark('bass')
    assert contexttools.get_effective_clef(t[5]) == contexttools.ClefMark('bass')
    assert contexttools.get_effective_clef(t[6]) == contexttools.ClefMark('bass')
    assert contexttools.get_effective_clef(t[7]) == contexttools.ClefMark('bass')
    assert contexttools.get_effective_clef(t[8]) == contexttools.ClefMark('bass')
    assert contexttools.get_effective_clef(t[9]) == contexttools.ClefMark('bass')

    assert t.format == '''\\new Staff {\n\t\\clef "treble"\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef "bass"\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\td'8\n\tef'8\n}'''
