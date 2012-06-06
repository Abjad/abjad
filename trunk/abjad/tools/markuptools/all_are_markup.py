from abjad.tools.markuptools.Markup import Markup


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

    return all([isinstance(x, Markup) for x in expr])
