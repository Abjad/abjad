from abjad import *
from experimental import *


def test_OffsetPositionedRhythmExpression_rotate_01():

    music = p("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = settingtools.OffsetPositionedRhythmExpression(music=music, voice_name='Voice 1')
    durations = [x.prolated_duration for x in expr.music[:]]
    beamtools.DuratedComplexBeamSpanner(expr.music[:], durations=durations, span=1)

    expr.rotate(-1)

    assert expr.music.lilypond_format == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\td'16 [\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\te'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n\t{\n\t\tc'16\n\t}\n}"


def test_OffsetPositionedRhythmExpression_rotate_02():

    music = p("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = settingtools.OffsetPositionedRhythmExpression(music=music, voice_name='Voice 1')
    durations = [x.prolated_duration for x in expr.music[:]]
    beamtools.DuratedComplexBeamSpanner(expr.music[:], durations=durations, span=1)

    expr.rotate(-2)

    assert expr.music.lilypond_format == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\te'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\td'16 ]\n\t}\n}"


def test_OffsetPositionedRhythmExpression_rotate_03():

    music = p("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = settingtools.OffsetPositionedRhythmExpression(music=music, voice_name='Voice 1')
    durations = [x.prolated_duration for x in expr.music[:]]
    beamtools.DuratedComplexBeamSpanner(expr.music[:], durations=durations, span=1)

    expr.rotate(-3)

    assert expr.music.lilypond_format == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tf'16 [\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\td'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\te'16 ]\n\t}\n}"


def test_OffsetPositionedRhythmExpression_rotate_04():
    '''Do not fracture beam.
    '''

    music = p("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = settingtools.OffsetPositionedRhythmExpression(music=music, voice_name='Voice 1')
    durations = [x.prolated_duration for x in expr.music[:]]
    beamtools.DuratedComplexBeamSpanner(expr.music[:], durations=durations, span=1)

    expr.rotate(-1, fracture_spanners=False)

    assert expr.music.lilypond_format == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\td'16 [\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\te'16\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tc''16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc'16 ]\n\t}\n}"


def test_OffsetPositionedRhythmExpression_rotate_05():
    '''Do not fracture beam.
    '''

    music = p("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = settingtools.OffsetPositionedRhythmExpression(music=music, voice_name='Voice 1')
    durations = [x.prolated_duration for x in expr.music[:]]
    beamtools.DuratedComplexBeamSpanner(expr.music[:], durations=durations, span=1)

    expr.rotate(-2, fracture_spanners=False)

    assert expr.music.lilypond_format == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\te'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tc''16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\td'16 ]\n\t}\n}"


def test_OffsetPositionedRhythmExpression_rotate_06():
    '''Do not fracture beam.
    '''

    music = p("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = settingtools.OffsetPositionedRhythmExpression(music=music, voice_name='Voice 1')
    durations = [x.prolated_duration for x in expr.music[:]]
    beamtools.DuratedComplexBeamSpanner(expr.music[:], durations=durations, span=1)

    expr.rotate(-3, fracture_spanners=False)

    assert expr.music.lilypond_format == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tf'16 [\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tc''16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tc'16\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\td'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\te'16 ]\n\t}\n}"


def test_OffsetPositionedRhythmExpression_rotate_07():
    '''Do not fracture beam. Zero effective rotation.
    '''
    
    music = p("{c'16 d'16} {e'16 f'16} {g'16 a'16} {b'16 c''16}")
    expr = settingtools.OffsetPositionedRhythmExpression(music=music, voice_name='Voice 1')
    durations = [x.prolated_duration for x in expr.music[:]]
    beamtools.DuratedComplexBeamSpanner(expr.music[:], durations=durations, span=1)

    expr.rotate(-8, fracture_spanners=False)

    assert expr.music.lilypond_format == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\td'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\te'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\ta'16\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tb'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc''16 ]\n\t}\n}"
