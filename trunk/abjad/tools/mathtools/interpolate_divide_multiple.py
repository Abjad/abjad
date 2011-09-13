from abjad.tools.mathtools.interpolate_divide import interpolate_divide


# TODO: fix hyphen chains in API entry so Sphinx doesn't complain.
def interpolate_divide_multiple(totals, key_values, exp='cosine'):
    '''.. versionadded:: 2.0

    Interpolate `key_values` such that the sum of the
    resulting interpolated values equals the given `totals`::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.interpolate_divide_multiple([100, 50], [20, 10, 20]) # doctest: +SKIP
        [19.4487, 18.5201, 16.2270, 13.7156, 11.7488, 10.4879,
        9.8515, 9.5130, 10.4213, 13.0736, 16.9918]

    The operation is the same as ``mathtools.interpolate_divide()``.
    But this function takes multiple `totals` and `key_values` at once.

    Precondition: ``len(totals) == len(key_values) - 1``.

    Set `totals` equal to a list or tuple of the total sum of interpolated values.

    Set `key_values` equal a list or tuple of key values to interpolate.

    Set `exp` to `consine` for consine interpolation.

    Set `exp` to a number for exponential interpolation.

    Returns a list of floats.

    .. versionchanged:: 2.0
        renamed ``interpolate.divide_multiple()`` to
        ``mathtools.interpolate_divide_multiple()``.
    '''

    # TODO: Here is the problematic example from the API entry.
    #    .      .     .    .  . ... .  .    .     .      .     .     .    .  . ...
    #    |--------------------|-------------------|---------------------|
    #            total[0]                    total[1]                total[2]
    #key_values[0]        key_values[1]         key_values[2]            key_values[3]

    assert len(totals) == len(key_values) - 1

    result = []
    for i in range(len(totals)):
        dts = interpolate_divide(totals[i], key_values[i], key_values[i+1], exp)
        # we want a flat list
        result.extend(dts)
    return result
