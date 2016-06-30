# -*- coding: utf-8 -*-


def list_pitch_numbers_in_expr(expr):
    '''Lists pitch numbers in `expr`.

    ::

        >>> tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        >>> pitchtools.list_pitch_numbers_in_expr(tuplet)
        (0, 2, 4)

    Returns tuple of zero or more numbers.
    '''
    from abjad.tools import pitchtools

    pitches = pitchtools.list_named_pitches_in_expr(expr)

    pitch_numbers = [pitch.pitch_number for pitch in pitches]
    pitch_numbers = tuple(pitch_numbers)

    return pitch_numbers