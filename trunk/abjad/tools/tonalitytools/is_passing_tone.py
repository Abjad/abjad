from abjad.tools.notetools.Note import Note
from abjad.tools import componenttools
from abjad.tools.tonalitytools.are_scalar_notes import are_scalar_notes


def is_passing_tone(note):
    r'''.. versionadded:: 2.0

    True when `note` is both preceeded and followed by scalewise
    sibling notes. Otherwise false. ::

        abjad> from abjad.tools import tonalitytools

    ::

        abjad> t = Staff("c'8 d'8 e'8 f'8")
        abjad> for note in t:
        ...     print '%s\t%s' % (note, tonalitytools.is_passing_tone(note))
        ...
        c'8     False
        d'8     True
        e'8     True
        f'8     False

    Return boolean.
    '''

    if not isinstance(note, Note):
        raise TypeError('must be note: %s' % note)

    try:
        prev_note = componenttools.get_nth_namesake_from_component(note, -1)
        next_note = componenttools.get_nth_namesake_from_component(note, 1)
    except IndexError:
        return False

    return are_scalar_notes(prev_note, note, next_note)
