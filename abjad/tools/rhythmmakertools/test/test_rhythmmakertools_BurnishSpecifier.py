import abjad
from abjad.tools import rhythmmakertools


def test_rhythmmakertools_BurnishSpecifier_01():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        left_classes=[abjad.Rest],
        right_classes=[abjad.Rest],
        left_counts=[2],
        right_counts=[1],
        )

    talea = rhythmmakertools.Talea(
        counts=[1, 1, 2, 4],
        denominator=32,
        )

    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        burnish_specifier=burnish_specifier,
        extra_counts_per_division=[0],
        )

    divisions = [(5, 16), (6, 16)]
    selections = rhythm_maker(divisions)

    maker = abjad.MeasureMaker()
    measures = maker(divisions)
    staff = abjad.Staff(measures)
    abjad.mutate(staff).replace_measure_contents(selections)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 5/16
                {
                    r32
                    r32
                    c'16 [
                    c'8
                    c'32 ]
                    r32
                }
            } % measure
            { % measure
                \time 6/16
                {
                    r16
                    r8
                    c'32 [
                    c'32
                    c'16 ]
                    r16
                }
            } % measure
        }
        '''
        )


def test_rhythmmakertools_BurnishSpecifier_02():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        left_classes=[0],
        middle_classes=[abjad.Rest],
        right_classes=[0],
        left_counts=[2],
        right_counts=[1],
        )

    talea = rhythmmakertools.Talea(
        counts=[1, 1, 2, 4],
        denominator=32,
        )

    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=[0],
        burnish_specifier=burnish_specifier,
        )

    divisions = [(5, 16), (6, 16)]
    selections = rhythm_maker(divisions)

    maker = abjad.MeasureMaker()
    measures = maker(divisions)
    staff = abjad.Staff(measures)
    abjad.mutate(staff).replace_measure_contents(selections)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 5/16
                {
                    c'32 [
                    c'32 ]
                    r16
                    r8
                    r32
                    c'32
                }
            } % measure
            { % measure
                \time 6/16
                {
                    c'16 [
                    c'8 ]
                    r32
                    r32
                    r16
                    c'16
                }
            } % measure
        }
        '''
        )


def test_rhythmmakertools_BurnishSpecifier_03():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        left_classes=[0],
        middle_classes=[abjad.Rest],
        right_classes=[0],
        left_counts=[2],
        right_counts=[1],
        )

    talea= rhythmmakertools.Talea(
        counts=[1, 1, 2, 4],
        denominator=32,
        )

    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=[3],
        burnish_specifier=burnish_specifier,
        )

    divisions = [(5, 16), (6, 16)]
    selections = rhythm_maker(divisions)

    maker = abjad.MeasureMaker()
    measures = maker(divisions)
    staff = abjad.Staff(measures)
    abjad.mutate(staff).replace_measure_contents(selections)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 5/16
                \tweak text #tuplet-number::calc-fraction-text
                \times 10/13 {
                    c'32 [
                    c'32 ]
                    r16
                    r8
                    r32
                    r32
                    r16
                    c'32 ~
                }
            } % measure
            { % measure
                \time 6/16
                \times 4/5 {
                    c'16. [
                    c'32 ]
                    r32
                    r16
                    r8
                    r32
                    r32
                    c'16
                }
            } % measure
        }
        '''
        )


def test_rhythmmakertools_BurnishSpecifier_04():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        left_classes=[abjad.Rest],
        right_classes=[abjad.Rest],
        left_counts=[1],
        right_counts=[1],
        )

    talea = rhythmmakertools.Talea(
        counts=[1, 1, 2, 4],
        denominator=32,
        )

    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=[0, 3],
        burnish_specifier=burnish_specifier,
        )

    divisions = [(5, 16), (6, 16)]
    selections = rhythm_maker(divisions)

    maker = abjad.MeasureMaker()
    measures = maker(divisions)
    staff = abjad.Staff(measures)
    abjad.mutate(staff).replace_measure_contents(selections)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 5/16
                {
                    r32
                    c'32 [
                    c'16
                    c'8
                    c'32 ]
                    r32
                }
            } % measure
            { % measure
                \time 6/16
                \times 4/5 {
                    r16
                    c'8 [
                    c'32
                    c'32
                    c'16
                    c'8 ]
                    r32
                }
            } % measure
        }
        '''
        )


def test_rhythmmakertools_BurnishSpecifier_05():

    burnish_specifier = rhythmmakertools.BurnishSpecifier(
        left_classes=[abjad.Rest],
        right_classes=[abjad.Rest],
        left_counts=[1],
        right_counts=[1],
        )

    talea = rhythmmakertools.Talea(
        counts=[1, 1, 2, 4],
        denominator=32,
        )

    rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=[0, 3],
        burnish_specifier=burnish_specifier,
        split_divisions_by_counts=[14],
        )

    divisions = [(5, 16), (6, 16)]
    selections = rhythm_maker(divisions)

    maker = abjad.MeasureMaker()
    measures = maker(divisions)
    staff = abjad.Staff(measures)
    abjad.mutate(staff).replace_measure_contents(selections)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 5/16
                {
                    r32
                    c'32 [
                    c'16
                    c'8
                    c'32 ]
                    r32
                }
            } % measure
            { % measure
                \time 6/16
                \times 4/7 {
                    r16
                    c'8
                    r32
                }
                {
                    r32
                    c'16 [
                    c'8 ]
                    r32
                }
            } % measure
        }
        '''
        )
