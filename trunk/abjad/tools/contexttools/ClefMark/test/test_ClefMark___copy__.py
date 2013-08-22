# -*- encoding: utf-8 -*-
from abjad import *


def test_ClefMark___copy___01():
    r'''Copies explicit clef marks copy.
    '''

    staff = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)
    contexttools.ClefMark('treble')(staff[0])
    contexttools.ClefMark('bass')(staff[4])
    copied_notes = mutate(staff[:2]).copy()
    staff.extend(copied_notes)

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

    assert inspect(staff).is_well_formed()
    assert inspect(staff[0]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert inspect(staff[1]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert inspect(staff[2]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert inspect(staff[3]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert inspect(staff[4]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert inspect(staff[5]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert inspect(staff[6]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert inspect(staff[7]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert inspect(staff[8]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert inspect(staff[9]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')


def test_ClefMark___copy___02():
    r'''Does not copy implicit clefs.
    '''

    staff = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)
    contexttools.ClefMark('treble')(staff[0])
    contexttools.ClefMark('bass')(staff[4])
    copied_notes = mutate(staff[2:4]).copy()
    staff.extend(copied_notes)

    assert inspect(staff).is_well_formed()
    assert inspect(staff[0]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert inspect(staff[1]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert inspect(staff[2]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert inspect(staff[3]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('treble')
    assert inspect(staff[4]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert inspect(staff[5]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert inspect(staff[6]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert inspect(staff[7]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert inspect(staff[8]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')
    assert inspect(staff[9]).get_effective_context_mark(contexttools.ClefMark) == contexttools.ClefMark('bass')

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
