import abjad


def test_makers_tuplet_from_ratio_and_pair_01():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 4), (6, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/7
        {
            c'16
            c'8
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_02():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 1, 2, 4), (6, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4
        {
            c'16
            c'16
            c'8
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_03():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((-2, 3, 7), (7, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 7/12
        {
            r8
            c'8.
            c'4..
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_04():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((7, 7, -4, -1), (1, 4))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \times 16/19
        {
            c'16..
            c'16..
            r16
            r64
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_05():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 2), (12, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_06():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((2, 4, 4), (12, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_07():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((4, 8, 8), (12, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_08():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((8, 16, 16), (12, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_09():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((2, 4, 4), (3, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5
        {
            c'16
            c'8
            c'8
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_10():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((2, 4, 4), (6, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_11():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((2, 4, 4), (12, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_12():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((2, 4, 4), (24, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_13():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 2), (6, 2))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5
        {
            c'2
            c'1
            c'1
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_14():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 2), (6, 4))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_15():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 2), (6, 8))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_16():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 2), (6, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5
        {
            c'16
            c'8
            c'8
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_17():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, -1, -1), (3, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 1/1
        {
            c'16
            r16
            r16
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_18():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 1, -1, -1), (4, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 1/1
        {
            c'16
            c'16
            r16
            r16
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_19():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 1, 1, -1, -1), (5, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 1/1
        {
            c'16
            c'16
            c'16
            r16
            r16
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_20():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 1, 1, 1, -1, -1), (6, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 1/1
        {
            c'16
            c'16
            c'16
            c'16
            r16
            r16
        }
        """
    )
