import pytest

import abjad


def test_LilyPondParser__spanners__Beam_01():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 8)]))
    abjad.beam(target[0:3])
    abjad.beam(target[3:], beam_lone_notes=True)

    assert abjad.lilypond(target) == abjad.string.normalize(
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
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__spanners__Beam_02():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 8)]))
    abjad.beam(target[:])
    abjad.beam(target[1:3])

    assert abjad.lilypond(target) == abjad.string.normalize(
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
        abjad.LilyPondParser()(abjad.lilypond(target))


def test_LilyPondParser__spanners__Beam_03():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 8)]))
    abjad.beam(target[:3])
    abjad.beam(target[2:])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c'8
            [
            c'8
            c'8
            [
            ]
            c'8
            ]
        }
        """
    )

    with pytest.raises(Exception):
        abjad.LilyPondParser()(abjad.lilypond(target))


def test_LilyPondParser__spanners__Beam_04():

    string = "{ c'8 [ c'8 c'8 c'8 }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Beam_05():
    """
    With direction.
    """

    maker = abjad.NoteMaker()
    target = abjad.Container(maker(4 * [0], [(1, 8)]))
    start_beam = abjad.StartBeam()
    abjad.attach(start_beam, target[0], direction=abjad.UP)
    stop_beam = abjad.StopBeam()
    abjad.attach(stop_beam, target[2])
    start_beam = abjad.StartBeam()
    abjad.attach(start_beam, target[3], direction=abjad.DOWN)
    stop_beam = abjad.StopBeam()
    abjad.attach(stop_beam, target[3])

    assert abjad.lilypond(target) == abjad.string.normalize(
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
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
