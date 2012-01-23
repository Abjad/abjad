from abjad.tools.componenttools.all_are_components import all_are_components
from abjad.tools.notetools.Note import Note


def all_are_notes(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad notes::

        abjad> notes = [Note("c'4"), Note("d'4"), Note("e'4")]

    ::

        abjad> notetools.all_are_notes(notes)
        True

    True when `expr` is an empty sequence::

        abjad> notetools.all_are_notes([])
        True

    Otherwise false::

        abjad> notetools.all_are_notes('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''

    return all_are_components(expr, klasses=(Note,))
