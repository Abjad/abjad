# -*- coding: utf-8 -*-


def transpose_pitch_expr_into_pitch_range(pitch_expr, pitch_range):
    '''Transposes `pitch_expr` into `pitch_range`.

    ::

        >>> pitches = [-2, -1, 13, 14]
        >>> range_ = pitchtools.PitchRange('[C4, C5]')
        >>> pitchtools.transpose_pitch_expr_into_pitch_range(pitches, range_)
        [10, 11, 1, 2]

    Returns new `pitch_expr` object.
    '''
    try:
        transposed_pitch_carriers = [
            _transpose_pitch_carrier_into_pitch_range(x, pitch_range)
            for x in pitch_expr
            ]
        return type(pitch_expr)(transposed_pitch_carriers)
    except TypeError:
        return _transpose_pitch_carrier_into_pitch_range(
            pitch_expr,
            pitch_range,
            )


# TODO: make public? make nested helper?
def _transpose_pitch_carrier_into_pitch_range(pitch_carrier, pitch_range):
    from abjad.tools import pitchtools
    while pitch_carrier < pitch_range:
        pitch_carrier = pitchtools.transpose_pitch_carrier_by_interval(
            pitch_carrier, 12)
    while pitch_range < pitch_carrier:
        pitch_carrier = pitchtools.transpose_pitch_carrier_by_interval(
            pitch_carrier, -12)
    if pitch_carrier not in pitch_range:
        message = 'can not transpose pitch carrier {!r} into pitch range.'
        message = message.format(pitch_carrier)
        raise ValueError(message)
    return pitch_carrier