from abjad.tools import durationtools


def is_beamable_component(expr):
    '''.. versionadded:: 1.1

    True when `expr` is a beamable component. Otherwise false::

        >>> beamtools.is_beamable_component(Note(13, (1, 16)))
        True

    Return boolean.

    .. versionchanged:: 2.9
        renamed ``componenttools.is_beamable_component()`` to
        ``beamtools.is_beamable_component()``.
    '''
    from abjad.tools import chordtools
    from abjad.tools import notetools

    if isinstance(expr, (notetools.Note, chordtools.Chord)):
        if 0 < durationtools.rational_to_flag_count(expr.written_duration):
            return True
    return False
