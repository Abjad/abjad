# -*- encoding: utf-8 -*-
import pytest
from experimental import *


def test_StartPositionedRhythmPayloadExpression_rotate_01():

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(
        durations=durations,
        span_beam_count=1,
        )
    attach(beam, expr.payload[:])

    expr.rotate(-1)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\td'16 [\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\te'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n\t{\n\t\tc'16\n\t}\n}"


def test_StartPositionedRhythmPayloadExpression_rotate_02():

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(
        durations=durations,
        span_beam_count=1,
        )
    attach(beam, expr.payload[:])


    expr.rotate(-2)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\te'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\td'16 ]\n\t}\n}"


def test_StartPositionedRhythmPayloadExpression_rotate_03():

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(
        durations=durations,
        span_beam_count=1,
        )
    attach(beam, expr.payload[:])

    expr.rotate(-3)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tf'16 [\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\td'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\te'16 ]\n\t}\n}"


def test_StartPositionedRhythmPayloadExpression_rotate_04():
    r'''Do not fracture beam.
    '''

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(
        durations=durations,
        span_beam_count=1,
        )
    attach(beam, expr.payload[:])

    expr.rotate(-1, fracture_spanners=False)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\td'16 [\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\te'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tc''16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc'16 ]\n\t}\n}"


def test_StartPositionedRhythmPayloadExpression_rotate_05():
    r'''Do not fracture beam.
    '''

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(durations=durations, span_beam_count=1)
    attach(beam, expr.payload[:])

    expr.rotate(-2, fracture_spanners=False)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\te'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tc''16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\td'16 ]\n\t}\n}"


def test_StartPositionedRhythmPayloadExpression_rotate_06():
    r'''Do not fracture beam.
    '''

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(
        durations=durations,
        span_beam_count=1,
        )
    attach(beam, expr.payload[:])

    expr.rotate(-3, fracture_spanners=False)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tf'16 [\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tc''16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\td'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\te'16 ]\n\t}\n}"


def test_StartPositionedRhythmPayloadExpression_rotate_07():
    r'''Do not fracture beam. Zero effective rotation.
    '''
    pytest.skip('is this causing an infinite loop because of get_duration()?')

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(
        durations=durations,
        span_beam_count=1,
        )
    attach(beam, expr.payload[:])

    expr.rotate(-8, fracture_spanners=False)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\td'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\te'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n}"


def test_StartPositionedRhythmPayloadExpression_rotate_08():
    r'''Rotation greater than component count.
    '''

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(
        durations=durations,
        span_beam_count=1,
        )
    attach(beam, expr.payload[:])

    expr.rotate(-9)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\td'16 [\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\te'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n\t{\n\t\tc'16\n\t}\n}"


def test_StartPositionedRhythmPayloadExpression_rotate_09():
    r'''Identity (zero) rotation.
    '''

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(
        durations=durations,
        span_beam_count=1,
        )
    attach(beam, expr.payload[:])

    expr.rotate(0)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\td'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\te'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n}"


def test_StartPositionedRhythmPayloadExpression_rotate_10():
    r'''Internal node zero-rotation.
    '''

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(
        durations=durations,
        span_beam_count=1,
        )
    attach(beam, expr.payload[:])

    rotation = musicexpressiontools.RotationExpression(0, 1)
    expr.rotate(rotation)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\td'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\te'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n}"


def test_StartPositionedRhythmPayloadExpression_rotate_11():
    r'''Internal node left rotation.
    '''

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(
        durations=durations,
        span_beam_count=1,
        )
    attach(beam, expr.payload[:])

    rotation = musicexpressiontools.RotationExpression(-1, 1)
    expr.rotate(rotation)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\te'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\td'16 ]\n\t}\n}"


def test_StartPositionedRhythmPayloadExpression_rotate_12():
    r'''Internal node left rotation.
    '''

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(
        durations=durations,
        span_beam_count=1,
        )
    attach(beam, expr.payload[:])

    rotation = musicexpressiontools.RotationExpression(-2, 1)
    expr.rotate(rotation)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\td'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\te'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tf'16 ]\n\t}\n}"


def test_StartPositionedRhythmPayloadExpression_rotate_13():
    r'''Internal node right rotation.
    '''

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(
        durations=durations,
        span_beam_count=1,
        )
    attach(beam, expr.payload[:])

    rotation = musicexpressiontools.RotationExpression(1, 1)
    expr.rotate(rotation)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\td'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\te'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\ta'16 ]\n\t}\n}"


def test_StartPositionedRhythmPayloadExpression_rotate_14():
    r'''Internal node right rotation.
    '''

    music = parse("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = musicexpressiontools.StartPositionedRhythmPayloadExpression(music, Offset(0))
    durations = [inspect_(x).get_duration() for x in expr.payload[:]]
    beam = spannertools.DuratedComplexBeam(
        durations=durations,
        span_beam_count=1,
        )
    attach(beam, expr.payload[:])

    rotation = musicexpressiontools.RotationExpression(2, 1)
    expr.rotate(rotation)

    # TODO: replace with TestManager.compare
    assert format(expr.payload) == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\td'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\te'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tf'16 ]\n\t}\n}"