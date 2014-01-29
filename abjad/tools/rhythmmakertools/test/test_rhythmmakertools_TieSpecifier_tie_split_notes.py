# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_TieSpecifier_tie_split_notes_01():

    talea = rhythmmakertools.Talea(
        counts=(5,), 
        denominator=16, 
        )
    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        )

    divisions = [(2, 8), (2, 8), (2, 8), (2, 8)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    measures = mutate(staff).replace_measure_contents(music)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'4 ~
            }
            {
                c'16 [
                c'8. ] ~
            }
            {
                c'8 [
                c'8 ] ~
            }
            {
                c'8. [
                c'16 ]
            }
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_rhythmmakertools_TieSpecifier_tie_split_notes_02():

    talea = rhythmmakertools.Talea(
        counts=(5,), 
        denominator=16, 
        )
    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        )

    divisions = [(3, 16), (5, 8), (4, 8), (7, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    measures = mutate(staff).replace_measure_contents(music)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/16
                c'8. ~
            }
            {
                \time 5/8
                c'8
                c'4 ~
                c'16 [
                c'8. ] ~
            }
            {
                \time 4/8
                c'8
                c'4 ~
                c'16 [
                c'16 ] ~
            }
            {
                \time 7/16
                c'4
                c'8.
            }
        }
        '''
        )

    assert inspect_(staff).is_well_formed()
