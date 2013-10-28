# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import iterationtools
from abjad.tools import pitchtools
from abjad.tools import voicetools


def notes_and_chords_are_in_range(expr):
    '''True when notes and chords in `expr` are 
    within traditional instrument ranges.

    ::

        >>> staff = Staff("c'8 r8 <d' fs'>8 r8")
        >>> violin = instrumenttools.Violin()
        >>> violin.attach(staff)
        Violin()(Staff{4})

    ::

        >>> instrumenttools.notes_and_chords_are_in_range(staff)
        True

    False otherwise:

    ::

        >>> staff = Staff("c'8 r8 <d fs>8 r8")
        >>> violin = instrumenttools.Violin()
        >>> violin.attach(staff)
        Violin()(Staff{4})

    ::

        >>> instrumenttools.notes_and_chords_are_in_range(staff)
        False

    Returns boolean.
    '''
    from abjad.tools import instrumenttools

    for note_or_chord in iterationtools.iterate_notes_and_chords_in_expr(expr):
        instrument = note_or_chord._get_effective_context_mark(
            instrumenttools.Instrument)
        if note_or_chord not in instrument._default_pitch_range:
            return False
    else:
        return True
