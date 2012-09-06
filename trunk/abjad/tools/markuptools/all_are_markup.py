def all_are_markup(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad markup::

        >>> markup = markuptools.Markup('some text')

    ::

        >>> markuptools.all_are_markup([markup])
        True

    True when `expr` is an empty sequence::

        >>> markuptools.all_are_markup([])
        True

    Otherwise false::

        >>> markuptools.all_are_markup('foo')
        False

    Return boolean.
    '''
    from abjad.tools import markuptools

    return all([isinstance(x, markuptools.Markup) for x in expr])
