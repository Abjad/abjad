from abjad.tools import componenttools


def all_are_notes(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad notes::

        >>> notes = [Note("c'4"), Note("d'4"), Note("e'4")]

    ::

        >>> notetools.all_are_notes(notes)
        True

    True when `expr` is an empty sequence::

        >>> notetools.all_are_notes([])
        True

    Otherwise false::

        >>> notetools.all_are_notes('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''
    from abjad.tools import notetools

    return componenttools.all_are_components(expr, klasses=(notetools.Note,))
