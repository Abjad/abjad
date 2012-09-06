from abjad.tools import componenttools


def all_are_scores(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad scores::

        >>> score = Score([Staff([Note("c'4")])])

    ::

        >>> score
        Score<<1>>

    ::

        >>> scoretools.all_are_scores([score])
        True

    True when `expr` is an empty sequence::

        >>> scoretools.all_are_scores([])
        True

    Otherwise false::

        >>> scoretools.all_are_scores('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''
    from abjad.tools import scoretools

    return componenttools.all_are_components(expr, klasses=(scoretools.Score,))
