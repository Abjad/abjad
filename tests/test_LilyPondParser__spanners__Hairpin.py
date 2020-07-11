import pytest

import abjad


def test_LilyPondParser__spanners__Hairpin_01():

    maker = abjad.NoteMaker()
    target = abjad.Staff(maker([0] * 5, [(1, 4)]))
    abjad.hairpin("< !", target[:3])
    abjad.hairpin("> ppp", target[2:])

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \<
            c'4
            c'4
            \!
            \>
            c'4
            c'4
            \ppp
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


# def test_LilyPondParser__spanners__Hairpin_02():
#
#    maker = abjad.NoteMaker()
#    target = abjad.Container(maker([0] * 4, [(1, 4)]))
#    abjad.hairpin('< !', target[0:2])
#    abjad.hairpin('< !', target[1:3])
#    abjad.hairpin('< !', target[2:])
#
#    assert abjad.lilypond(target) == abjad.String.normalize(
#        r"""
#        {
#            c'4
#            \<
#            c'4
#            \!
#            \<
#            c'4
#            \!
#            \<
#            c'4
#            \!
#        }
#        """
#        )
#
#    string = r"""\relative c' { c \< c \< c \< c \! }"""
#    parser = abjad.parser.LilyPondParser()
#    result = parser(string)
#    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__spanners__Hairpin_02():
    """
    Dynamics can terminate hairpins.
    """

    maker = abjad.NoteMaker()
    target = abjad.Staff(maker([0] * 3, [(1, 4)]))
    abjad.hairpin("<", target[0:2])
    abjad.hairpin("p > f", target[1:])

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \<
            c'4
            \p
            \>
            c'4
            \f
        }
        """
    )

    string = r"\new Staff \relative c' { c \< c \p \> c \f }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__spanners__Hairpin_03():
    """
    Unterminated.
    """

    string = r"{ c \< c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Hairpin_04():
    """
    Unbegun is okay.
    """

    string = r"{ c c c c \! }"
    abjad.parser.LilyPondParser()(string)


def test_LilyPondParser__spanners__Hairpin_05():
    """
    No double dynamic spans permitted.
    """

    string = r"{ c \< \> c c c \! }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Hairpin_06():
    """
    With direction.
    """

    maker = abjad.NoteMaker()
    target = abjad.Staff(maker([0] * 5, [(1, 4)]))
    start_hairpin = abjad.StartHairpin("<", direction=abjad.Up)
    abjad.attach(start_hairpin, target[0])
    stop_hairpin = abjad.StopHairpin()
    abjad.attach(stop_hairpin, target[2])
    hairpin = abjad.StartHairpin(">", direction=abjad.Down)
    abjad.attach(hairpin, target[2])
    dynamic = abjad.Dynamic("ppp")
    abjad.attach(dynamic, target[-1])

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            ^ \<
            c'4
            c'4
            \!
            _ \>
            c'4
            c'4
            \ppp
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__spanners__Hairpin_07():

    string = r"\new Staff { c'4 ( \p \< d'4 e'4 f'4 ) \! }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(result) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \p
            \<
            (
            d'4
            e'4
            f'4
            \!
            )
        }
        """
    )
