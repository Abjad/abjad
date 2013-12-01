# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.topleveltools import iterate


def notes_and_chords_are_in_range(expr):
    '''True when notes and chords in `expr` are 
    within traditional instrument ranges.

    ::

        >>> staff = Staff("c'8 r8 <d' fs'>8 r8")
        >>> violin = instrumenttools.Violin()
        >>> attach(violin, staff)

    ::

        >>> instrumenttools.notes_and_chords_are_in_range(staff)
        True

    Otherwise false:

    ::

        >>> staff = Staff("c'8 r8 <d fs>8 r8")
        >>> violin = instrumenttools.Violin()
        >>> attach(violin, staff)

    ::

        >>> instrumenttools.notes_and_chords_are_in_range(staff)
        False

    Returns boolean.
    '''
    from abjad.tools import instrumenttools

    for note_or_chord in iterate(expr).by_class(
        (scoretools.Note, scoretools.Chord)):
        instrument = note_or_chord._get_effective_indicator(
            instrumenttools.Instrument)
        if note_or_chord not in instrument._default_pitch_range:
            return False
    else:
        return True
