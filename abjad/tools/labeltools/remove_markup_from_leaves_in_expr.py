# -*- coding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import iterate


def remove_markup_from_leaves_in_expr(expr):
    r'''Removes markup from leaves in `expr`.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> label(staff).with_pitches(prototype=pitchtools.NumberedPitchClass)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            c'8 ^ \markup { \small 0 }
            d'8 ^ \markup { \small 2 }
            e'8 ^ \markup { \small 4 }
            f'8 ^ \markup { \small 5 }
        }

    ::

        >>> labeltools.remove_markup_from_leaves_in_expr(staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    Returns none.
    '''
    from abjad.tools import markuptools

    for leaf in iterate(expr).by_class(scoretools.Leaf):
        detach(markuptools.Markup, leaf)