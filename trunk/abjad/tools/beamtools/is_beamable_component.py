from abjad.tools import chordtools
from abjad.tools import durationtools
from abjad.tools import notetools


def is_beamable_component(expr):
    '''.. versionadded:: 1.1

    True when `expr` is a beamable component. Otherwise false::

        >>> beamtools.is_beamable_component(Note(13, (1, 16)))
        True

    Return boolean.
    '''

    if isinstance(expr, (notetools.Note, chordtools.Chord)):
        if 0 < expr.written_duration.flag_count:
            return True
    return False
