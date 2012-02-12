def is_beamable_component(expr):
    '''.. versionadded:: 1.1

    True when `expr` is a beamable component. Otherwise false::

        abjad> componenttools.is_beamable_component(Note(13, (1, 16)))
        True

    Return boolean.
    '''
    from abjad.tools.chordtools.Chord import Chord
    from abjad.tools.notetools.Note import Note
    from abjad.tools import durationtools

    if isinstance(expr, (Note, Chord)):
        if 0 < durationtools.rational_to_flag_count(expr.written_duration):
            return True
    return False
