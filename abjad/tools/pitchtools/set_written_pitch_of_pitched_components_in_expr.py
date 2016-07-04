# -*- coding: utf-8 -*-
from abjad.tools.topleveltools import iterate


def set_written_pitch_of_pitched_components_in_expr(expr, written_pitch=0):
    r'''Sets written pitch of pitched components in `expr` to `written_pitch`.

    ::

        >>> staff = Staff("c' d' e' f'")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    ::

        >>> pitchtools.set_written_pitch_of_pitched_components_in_expr(staff)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'4
            c'4
            c'4
            c'4
        }

    Use as a way of neutralizing pitch information in an arbitrary piece of score.

    Returns none.
    '''
    from abjad.tools import scoretools

    for leaf in iterate(expr).by_class(scoretools.Leaf):
        if isinstance(leaf, scoretools.Note):
            leaf.written_pitch = written_pitch
        elif isinstance(leaf, scoretools.Chord):
            leaf.written_pitches = [written_pitch]