# -*- coding: utf-8 -*-
import pytest
import sys
from abjad import *


def test_rhythmmakertools_BurnishSpecifier_outer_divisions_only_01():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        left_classes=(0,),
        middle_classes=(-1,),
        right_classes=(0,),
        left_counts=(1,),
        right_counts=(1,),
        outer_divisions_only=True,
        )

    talea = rhythmmakertools.Talea(
        counts=(1,),
        denominator=16,
        )

    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        burnish_specifier=burnish_specifier,
        extra_counts_per_division=(2,),
        )

    divisions = [(3, 16), (3, 8)]
    selections = rhythm_maker(divisions)

    selections = sequencetools.flatten_sequence(selections)
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(selections)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/16
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    c'16
                    r16
                    r16
                    r16
                    r16
                }
            }
            {
                \time 3/8
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    r16
                    r16
                    r16
                    r16
                    r16
                    r16
                    r16
                    c'16
                }
            }
        }
        '''
        ), format(staff)


def test_rhythmmakertools_BurnishSpecifier_outer_divisions_only_02():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        left_classes=(-1,),
        right_classes=(-1,),
        left_counts=(1,),
        right_counts=(1,),
        outer_divisions_only=True,
        )

    talea = rhythmmakertools.Talea(
        counts=(1,),
        denominator=4,
        )

    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        burnish_specifier=burnish_specifier,
        extra_counts_per_division=(2,),
        )

    divisions = [(3, 16), (3, 8)]
    selections = rhythm_maker(divisions)

    selections = sequencetools.flatten_sequence(selections)
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(selections)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/16
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    r4
                    c'16 ~
                }
            }
            {
                \time 3/8
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    c'8.
                    c'4
                    r16
                }
            }
        }
        '''
        ), format(staff)


@pytest.mark.skipif(sys.version_info[0] == 3, reason='Broken under Py3.')
def test_rhythmmakertools_BurnishSpecifier_outer_divisions_only_03():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        left_classes=(-1,),
        right_classes=(-1,),
        left_counts=(1,),
        right_counts=(1,),
        outer_divisions_only=True,
        )

    talea = rhythmmakertools.Talea(
        counts=(1, 2, 3),
        denominator=16,
        )

    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        burnish_specifier=burnish_specifier,
        extra_counts_per_division=(0, 2),
        split_divisions_by_counts=(9,),
        )

    divisions = [(3, 8), (4, 8)]
    selections = rhythm_maker(divisions)

    selections = sequencetools.flatten_sequence(selections)
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(selections)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 3/8
                {
                    r16
                    c'8 [
                    c'8. ]
                }
            }
            {
                \time 4/8
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    c'16 [
                    c'8
                    c'8 ~ ]
                }
                {
                    c'16 [
                    c'16
                    c'8 ]
                    r16
                }
            }
        }
        '''
        ), format(staff)


def test_rhythmmakertools_BurnishSpecifier_outer_divisions_only_04():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        left_classes=(-1,),
        right_classes=(-1,),
        left_counts=(1,),
        right_counts=(2,),
        outer_divisions_only=True,
        )

    talea = rhythmmakertools.Talea(
        counts=(1,),
        denominator=8,
        )

    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        burnish_specifier=burnish_specifier,
        extra_counts_per_division=(),
        )

    divisions = [(8, 8)]
    selections = rhythm_maker(divisions)

    selections = sequencetools.flatten_sequence(selections)
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    mutate(staff).replace_measure_contents(selections)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 8/8
                r8
                c'8 [
                c'8
                c'8
                c'8
                c'8 ]
                r8
                r8
            }
        }
        '''
        ), format(staff)