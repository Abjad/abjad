import pytest

import abjad


def test_LilyPondParser__spanners__Beam_01():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 8)]))
    abjad.beam(target[0:3])
    abjad.beam(target[3:], beam_lone_notes=True)

    assert format(target) == abjad.String.normalize(
        r"""
        {
            c'8
            [
            c'8
            c'8
            ]
            c'8
            [
            ]
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_LilyPondParser__spanners__Beam_02():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 8)]))
    abjad.beam(target[:])
    abjad.beam(target[1:3])

    assert format(target) == abjad.String.normalize(
        r"""
        {
            c'8
            [
            c'8
            [
            c'8
            ]
            c'8
            ]
        }
        """
    )

    with pytest.raises(Exception):
        abjad.LilyPondParser()(format(target))


def test_LilyPondParser__spanners__Beam_03():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 8)]))
    abjad.beam(target[:3])
    abjad.beam(target[2:])

    assert format(target) == abjad.String.normalize(
        r"""
        {
            c'8
            [
            c'8
            c'8
            ]
            [
            c'8
            ]
        }
        """
    )

    with pytest.raises(Exception):
        abjad.LilyPondParser()(format(target))


def test_LilyPondParser__spanners__Beam_04():

    string = "{ c'8 [ c'8 c'8 c'8 }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Beam_05():
    """
    With direction.
    """

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 8)]))
    start_beam = abjad.StartBeam(direction=abjad.Up)
    abjad.beam(target[0:3], start_beam=start_beam)
    start_beam = abjad.StartBeam(direction=abjad.Down)
    abjad.beam(target[3:], start_beam=start_beam, beam_lone_notes=True)

    assert format(target) == abjad.String.normalize(
        r"""
        {
            c'8
            ^ [
            c'8
            c'8
            ]
            c'8
            _ [
            ]
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
