from abjad.tools.mathtools.sign import sign


def cumulative_signed_weights(sequence):
    '''Cumulative signed weights of `sequence`::

        abjad> from abjad.tools import mathtools

    ::

        abjad> l = [1, -2, -3, 4, -5, -6, 7, -8, -9, 10]
        abjad> mathtools.cumulative_signed_weights(l)
        [1, -3, -6, 10, -15, -21, 28, -36, -45, 55]

    Raise type error when `sequence` is not a list.

    For cumulative (unsigned) weights use ``mathtools.cumulative_sums([abs(x) for x in l])``.

    Return list.

    .. versionchanged:: 2.0
        renamed ``sequencetools.cumulative_weights_signed()`` to
        ``mathtools.cumulative_signed_weights()``.
    '''

    if not isinstance(sequence, list):
        raise TypeError

    result = []

    for x in sequence:
        try:
            next = abs(prev) + abs(x)
            prev_sign = sign(prev)
        except NameError:
            next = abs(x)
            prev_sign = 0
        sign_x = sign(x)
        if sign_x == -1:
            next *= sign_x
        elif sign_x == 0:
            next *= prev_sign
        #yield next
        result.append(next)
        prev = next

    #raise StopIteration
    return result
