# -*- encoding: utf-8 -*-
from abjad import *


def test_ClefMark___copy___01():
    r'''Clef marks copy.
    '''

    staff = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)
    contexttools.ClefMark('treble')(staff[0])
    contexttools.ClefMark('bass')(staff[4])
    staff.extend(componenttools.copy_components_and_immediate_parent_of_first_component(staff[:2]))

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

    assert select(staff).is_well_formed()
    assert more(staff[0]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert more(staff[1]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert more(staff[2]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert more(staff[3]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert more(staff[4]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert more(staff[5]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert more(staff[6]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert more(staff[7]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert more(staff[8]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert more(staff[9]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')

    assert testtools.compare(
        staff,
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
        )


def test_ClefMark___copy___02():
    r'''Implicit clefs do not copy.
    '''

    staff = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)
    contexttools.ClefMark('treble')(staff[0])
    contexttools.ClefMark('bass')(staff[4])
    staff.extend(componenttools.copy_components_and_immediate_parent_of_first_component(staff[2:4]))

    assert select(staff).is_well_formed()
    assert more(staff[0]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert more(staff[1]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert more(staff[2]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert more(staff[3]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert more(staff[4]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert more(staff[5]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert more(staff[6]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert more(staff[7]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert more(staff[8]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert more(staff[9]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')

    assert testtools.compare(
        staff,
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
            d'8
            ef'8
        }
        '''
        )
