# -*- encoding: utf-8 -*-
from abjad import *


def test_ClefMark___copy___01():
    r'''Clef marks copy.
    '''

    t = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(t)
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

    assert select(t).is_well_formed()
    assert t[0].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert t[1].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert t[2].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert t[3].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert t[4].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert t[5].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert t[6].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert t[7].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert t[8].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert t[9].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')

    assert testtools.compare(
        t.lilypond_format,
        '''\\new Staff {\n\t\\clef "treble"\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef "bass"\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\t\\clef "treble"\n\tc'8\n\tcs'8\n}'''
        )


def test_ClefMark___copy___02():
    r'''Implicit clefs do not copy.
    '''

    t = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(t)
    contexttools.ClefMark('treble')(t[0])
    contexttools.ClefMark('bass')(t[4])
    t.extend(componenttools.copy_components_and_immediate_parent_of_first_component(t[2:4]))

    assert select(t).is_well_formed()
    assert t[0].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert t[1].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert t[2].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert t[3].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert t[4].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert t[5].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert t[6].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert t[7].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert t[8].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert t[9].get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')

    assert testtools.compare(
        t.lilypond_format,
        '''\\new Staff {\n\t\\clef "treble"\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef "bass"\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\td'8\n\tef'8\n}'''
        )
