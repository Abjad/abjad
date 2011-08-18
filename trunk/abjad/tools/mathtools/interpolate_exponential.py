def interpolate_exponential(y1, y2, mu, exp = 1):
    '''Exponential interpolate `y1` and `y2` with `mu` normalized ``[0, 1]``::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.interpolate_exponential(0, 1, 0.5, 4)
        0.0625

    Set `exp` equal to the exponent of interpolation.

    Return float.

    .. versionchanged:: 2.0
        renamed ``interpolate.exponential()`` to
        ``mathtools.interpolate_exponential()``.
    '''

    return (y1 * (1 - mu ** exp) + y2 * mu ** exp)
