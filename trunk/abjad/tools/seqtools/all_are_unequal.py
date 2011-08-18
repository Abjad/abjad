def all_are_unequal(expr):
    '''.. versionadded:: 1.1

    True when `expr` is a sequence all elements in `expr` are unequal::

        abjad> from abjad.tools import seqtools

    ::

        abjad> seqtools.all_are_unequal([1, 2, 3, 4, 9])
        True

    True when `expr` is an empty sequence::

        abjad> seqtools.all_are_unequal([ ])
        True

    False otherwise::

        abjad> seqtools.all_are_unequal(17)
        False

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``seqtools.is_unique()`` to
        ``seqtools.all_are_unequal()``.
    '''

    try:
        return expr == type(expr)(set(expr))
    except TypeError:
        return False
