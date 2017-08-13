import abjad


def test_scoretools_Tuplet_set_minimum_denominator_01():

    tuplet = abjad.Tuplet(abjad.Multiplier(3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplet.set_minimum_denominator(8)

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/10 {
            c'4
            d'8
            e'8
            f'4
            g'2
        }
        '''
        )

    assert abjad.inspect(tuplet).is_well_formed()


def test_scoretools_Tuplet_set_minimum_denominator_02():

    tuplet = abjad.Tuplet(abjad.Multiplier(3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplet.set_minimum_denominator(16)

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 12/20 {
            c'4
            d'8
            e'8
            f'4
            g'2
        }
        '''
        )

    assert abjad.inspect(tuplet).is_well_formed()


def test_scoretools_Tuplet_set_minimum_denominator_03():

    tuplet = abjad.Tuplet(abjad.Multiplier(3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplet.set_minimum_denominator(2)

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'4
            d'8
            e'8
            f'4
            g'2
        }
        '''
        )

    assert abjad.inspect(tuplet).is_well_formed()
