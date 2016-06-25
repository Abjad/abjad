# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.topleveltools import iterate


def notes_and_chords_are_in_range(expr):
    '''Is true when notes and chords in `expr` are within traditional
    instrument ranges.

    ..  todo:: Move to WellformednessManager.

    ..  container:: example

        **Example 1.** In range:

        ::

            >>> staff = Staff("c'8 r8 <d' fs'>8 r8")
            >>> violin = instrumenttools.Violin()
            >>> attach(violin, staff)
            >>> show(staff) # doctest: +SKIP

        ::

            >>> instrumenttools.notes_and_chords_are_in_range(staff)
            True

    ..  container:: example

        **Example 2.** Out of range:

        ::

            >>> staff = Staff("c'8 r8 <d fs>8 r8")
            >>> violin = instrumenttools.Violin()
            >>> attach(violin, staff)
            >>> show(staff) # doctest: +SKIP

        ::

            >>> instrumenttools.notes_and_chords_are_in_range(staff)
            False

    Returns true or false.
    '''
    from abjad.tools import instrumenttools
    prototype = (scoretools.Note, scoretools.Chord)
    for note_or_chord in iterate(expr).by_class(prototype):
        instrument = note_or_chord._get_effective(instrumenttools.Instrument)
        if note_or_chord not in instrument.pitch_range:
            return False
    else:
        return True