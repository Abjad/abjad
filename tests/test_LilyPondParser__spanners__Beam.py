import abjad
import pytest


def test_LilyPondParser__spanners__Beam_01():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 8)]))
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, target[0:3])
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, target[3:])

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
    """
    With start and stop reversed.
    """

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 8)]))
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, target[0:3])
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, target[3:])

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

    string = r"""\relative c' { c8 [ c c ] c ] [ }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_LilyPondParser__spanners__Beam_03():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 8)]))
    beam = abjad.Beam()
    abjad.attach(beam, target[:])
    beam = abjad.Beam()
    abjad.attach(beam, target[1:3])

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

    assert pytest.raises(Exception, "LilyPondParser()(format(target))")


def test_LilyPondParser__spanners__Beam_04():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 8)]))
    beam = abjad.Beam()
    abjad.attach(beam, target[:3])
    beam = abjad.Beam()
    abjad.attach(beam, target[2:])

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

    assert pytest.raises(Exception, "LilyPondParser()(format(target))")


def test_LilyPondParser__spanners__Beam_05():

    string = "{ c'8 [ c'8 c'8 c'8 }"
    assert pytest.raises(Exception, "LilyPondParser()(string)")


def test_LilyPondParser__spanners__Beam_06():

    string = "{ c'8 c'8 c'8 c'8 ] }"
    result = abjad.parser.LilyPondParser()(string)
    assert not abjad.inspect(result[-1]).spanners()


def test_LilyPondParser__spanners__Beam_07():
    """
    With direction.
    """

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 8)]))
    beam = abjad.Beam(beam_lone_notes=True, direction=abjad.Up)
    abjad.attach(beam, target[0:3])
    beam = abjad.Beam(beam_lone_notes=True, direction=abjad.Down)
    abjad.attach(beam, target[3:])

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
