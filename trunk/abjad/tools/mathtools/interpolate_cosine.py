import math


def interpolate_cosine(y1, y2, mu):
    '''Cosine interpolate `y1` and `y2` with `mu` normalized ``[0, 1]``::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.interpolate_cosine(0, 1, 0.5)
        0.49999999999999994

    Return float.

    .. versionchanged:: 2.0
        renamed ``interpolate.cosine()`` to
        ``mathtools.interpolate_cosine()``.
    '''

    mu2 = (1 - math.cos(mu * math.pi)) / 2
    return (y1 * (1 - mu2) + y2 * mu2)
