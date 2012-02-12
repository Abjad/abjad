from abjad.tools.pitchtools.transpose_pitch_carrier_by_melodic_interval import transpose_pitch_carrier_by_melodic_interval


def transpose_pitch_expr_into_pitch_range(pitch_expr, pitch_range):
    '''.. versionadded:: 2.0

    Transpose `pitch_expr` into `pitch_range`::

        abjad> pitchtools.transpose_pitch_expr_into_pitch_range([-2, -1, 13, 14], pitchtools.PitchRange(0, 12))
        [10, 11, 1, 2]

    Return new `pitch_expr` object.
    '''

    try:
        transposed_pitch_carriers = [_transpose_pitch_carrier_into_pitch_range(x, pitch_range) for x in pitch_expr]
        return type(pitch_expr)(transposed_pitch_carriers)
    except TypeError:
        return _transpose_pitch_carrier_into_pitch_range(pitch_expr, pitch_range)


def _transpose_pitch_carrier_into_pitch_range(pitch_carrier, pitch_range):
    while pitch_carrier < pitch_range:
        pitch_carrier = transpose_pitch_carrier_by_melodic_interval(pitch_carrier, 12)
    while pitch_range < pitch_carrier:
        pitch_carrier = transpose_pitch_carrier_by_melodic_interval(pitch_carrier, -12)
    if pitch_carrier not in pitch_range:
        raise ValueError('can not transpose pitch carrier %s into pitch range.' % pitch_carrier)
    return pitch_carrier
