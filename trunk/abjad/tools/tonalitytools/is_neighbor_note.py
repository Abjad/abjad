from abjad.tools import notetools
from abjad.tools import componenttools


def is_neighbor_note(note):
    r'''.. versionadded:: 2.0

    True when `note` is preceeded by a stepwise interval in one direction
    and followed by a stepwise interval in the other direction.
    Otherwise false. ::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> for note in t:
        ...     print '%s\t%s' % (note, tonalitytools.is_neighbor_note(note))
        ...
        c'8     False
        d'8     False
        e'8     False
        f'8     False

    Return boolean.
    '''
    from abjad.tools import tonalitytools

    if not isinstance(note, notetools.Note):
        raise TypeError('must be note: %s' % note)

    try:
        previous_note = componenttools.get_nth_namesake_from_component(note, -1)
        next_note = componenttools.get_nth_namesake_from_component(note, 1)
    except IndexError:
        return False

    notes = [previous_note, note, next_note]

    return tonalitytools.are_stepwise_notes(notes) and not tonalitytools.are_scalar_notes(notes)
