from abjad.tools.componenttools.all_are_components import all_are_components
from abjad.tools.chordtools.Chord import Chord
from abjad.decorators import requires


@requires(object)
def all_are_chords(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad chords::

        abjad> chords = [Chord("<c' e' g'>4"), Chord("<c' f' a'>4")]

    ::

        abjad> chordtools.all_are_chords(chords)
        True

    True when `expr` is an empty sequence::

        abjad> chordtools.all_are_chords([])
        True

    Otherwise false::

        abjad> chordtools.all_are_chords('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''

    return all_are_components(expr, klasses=(Chord,))
