from abjad.tools import componenttools
from abjad.tools import decoratortools


@decoratortools.requires(object)
def all_are_chords(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad chords::

        >>> chords = [Chord("<c' e' g'>4"), Chord("<c' f' a'>4")]

    ::

        >>> chordtools.all_are_chords(chords)
        True

    True when `expr` is an empty sequence::

        >>> chordtools.all_are_chords([])
        True

    Otherwise false::

        >>> chordtools.all_are_chords('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''
    from abjad.tools import chordtools

    return componenttools.all_are_components(expr, klasses=(chordtools.Chord,))
