from abjad.tools import componenttools
from abjad.tools import mathtools
from abjad.tools import notetools


def is_neighbor_note(note):
    r'''.. versionadded:: 2.0

    True when `note` is preceeded by a stepwise interval in one direction
    and followed by a stepwise interval in the other direction.
    Otherwise false:

    ::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> for note in t:
        ...     print '%s\t%s' % (note, tonalanalysistools.is_neighbor_note(note))
        ...
        c'8     False
        d'8     False
        e'8     False
        f'8     False

    Return boolean.
    '''
    from abjad.tools import tonalanalysistools

    if not isinstance(note, notetools.Note):
        raise TypeError('must be note: {!r}.'.format(note))

    previous_note = note._get_namesake(-1)
    next_note = note._get_namesake(1)

    if previous_note is None:
        return False
    if next_note is None:
        return False

    notes = [previous_note, note, next_note]
    selection = tonalanalysistools.select(notes)

    preceding_interval = note.written_pitch - previous_note.written_pitch
    preceding_interval_direction = \
        mathtools.sign(preceding_interval.direction_number)
    following_interval = next_note.written_pitch - note.written_pitch
    following_interval_direction = \
        mathtools.sign(following_interval.direction_number)

    if selection.are_stepwise_notes():
        if preceding_interval_direction != following_interval_direction:
            return True

    return False
