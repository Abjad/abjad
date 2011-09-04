def is_restricted_growth_function(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a sequence and `expr` meets the criteria for a restricted
    growth function::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.is_restricted_growth_function([1, 1, 1, 1])
        True

    ::


        abjad> sequencetools.is_restricted_growth_function([1, 1, 1, 2])
        True

    ::

        abjad> sequencetools.is_restricted_growth_function([1, 1, 2, 1])
        True

    ::

        abjad> sequencetools.is_restricted_growth_function([1, 1, 2, 2])
        True

    Otherwise false::

        abjad> sequencetools.is_restricted_growth_function([1, 1, 1, 3])
        False

    ::

        abjad> sequencetools.is_restricted_growth_function(17)
        False

    A restricted growth function is a sequence ``l`` such that ``l[0] == 1``
    and such that ``l[i] <= max(l[:i]) + 1`` for ``1 <= i <= len(l)``.

    Return boolean.
    '''

    try:
        for i, n in enumerate(expr):
            if i == 0:
                if not n == 1:
                    return False
            else:
                if not n <= max(expr[:i]) + 1:
                    return False
        return True
    except TypeError:
        return False
