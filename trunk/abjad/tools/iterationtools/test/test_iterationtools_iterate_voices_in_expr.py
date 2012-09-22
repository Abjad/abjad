from abjad import *


def test_iterationtools_iterate_voices_in_expr_01():

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("c'4 b4")
    staff = Staff([voice_1, voice_2])
    staff.is_parallel = True

    voices = iterationtools.iterate_voices_in_expr(staff, reverse=True)
    voices = list(voices)

    assert voices[0] is voice_2
    assert voices[1] is voice_1


def test_iterationtools_iterate_voices_in_expr_02():

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("c'4 b4")
    staff = Staff([voice_1, voice_2])
    staff.is_parallel = True

    voices = iterationtools.iterate_voices_in_expr(staff)
    voices = list(voices)

    assert voices[0] is voice_1
    assert voices[1] is voice_2
