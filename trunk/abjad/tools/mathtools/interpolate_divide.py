# TODO: eliminate string-valued exp='cosine' keyword
def interpolate_divide(total, start_fraction, stop_fraction, exp='cosine'):
    '''Divide `total` into segments of sizes computed from interpolating
    between `start_fraction` and `stop_fraction`::

        >>> from abjad.tools import mathtools

    ::

        >>> mathtools.interpolate_divide(10, 1, 1, exp=1)
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> sum(mathtools.interpolate_divide(10, 1, 1, exp=1))
        10.0

    ::

        >>> mathtools.interpolate_divide(10, 5, 1) # doctest: +SKIP
        [4.7986734489043181, 2.8792040693425909, 1.3263207210948171,
        0.99580176065827419]
        >>> sum(mathtools.interpolate_divide(10, 5, 1))
        10.0

    Set ``exp='cosine'`` for cosine interpolation.

    Set `exp` to a numeric value for exponential interpolation with `exp`
    as the exponent.

    Scale resulting segments so that their sum equals exactly `total`.

    Return a list of floats.

    .. versionchanged:: 2.0
        renamed ``interpolate.divide()`` to
        ``mathtools.interpolate_divide()``.
    '''
    from abjad.tools import mathtools

    if total <=0 :
        raise ValueError("'total' must be positive.")
    if start_fraction <= 0 or stop_fraction <= 0:
        raise ValueError("Both 'start_fraction' and 'stop_fraction' must be positive.")
    if total < (stop_fraction + start_fraction):
        raise ValueError("'start_fraction' + 'stop_fraction' must be < 'total'.")

    result = []
    total = float(total)
    partial_sum = 0
    while partial_sum < total:
        if exp == 'cosine':
            ip = mathtools.interpolate_cosine(start_fraction, stop_fraction, partial_sum / total)
        else:
            ip = mathtools.interpolate_exponential(start_fraction, stop_fraction, partial_sum / total, exp)
        result.append(ip)
        partial_sum += ip

    # scale result to fit total exaclty
    result = [x * total / sum(result) for x in result]
    return result
