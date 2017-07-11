# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import iterate


def notes_and_chords_are_on_expected_clefs(
    argument,
    percussion_clef_is_allowed=True,
    ):
    r'''Is true when notes and chords in `argument` are on expected clefs.

    ::

        >>> import abjad

    ..  todo:: Move to WellformednessManager.

    ..  container:: example

        Expected clef:

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> clef = abjad.Clef(name='treble')
            >>> abjad.attach(clef, staff)
            >>> violin = abjad.instrumenttools.Violin()
            >>> abjad.attach(violin, staff)
            >>> show(staff) # doctest: +SKIP

        ::

            >>> abjad.instrumenttools.notes_and_chords_are_on_expected_clefs(staff)
            True

    ..  container:: example

        Unexpected clef:

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> clef = abjad.Clef(name='alto')
            >>> abjad.attach(clef, staff)
            >>> violin = abjad.instrumenttools.Violin()
            >>> abjad.attach(violin, staff)
            >>> show(staff) # doctest: +SKIP

        ::

            >>> abjad.instrumenttools.notes_and_chords_are_on_expected_clefs(staff)
            False

    ..  container:: example

        Allows percussion clef:

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> clef = abjad.Clef(name='percussion')
            >>> abjad.attach(clef, staff)
            >>> violin = abjad.instrumenttools.Violin()
            >>> abjad.attach(violin, staff)
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \clef "percussion"
                \set Staff.instrumentName = \markup { Violin }
                \set Staff.shortInstrumentName = \markup { Vn. }
                c'8
                d'8
                e'8
                f'8
            }

        ::

            >>> abjad.instrumenttools.notes_and_chords_are_on_expected_clefs(
            ...     staff, percussion_clef_is_allowed=True)
            True

    ..  container:: example

        Forbids percussion clef:

        ::

            >>> abjad.instrumenttools.notes_and_chords_are_on_expected_clefs(
            ...     staff, percussion_clef_is_allowed=False)
            False

    Returns true or false.
    '''
    from abjad.tools import instrumenttools
    prototype = (scoretools.Note, scoretools.Chord)
    for note_or_chord in iterate(argument).by_class(prototype):
        instrument = note_or_chord._get_effective(instrumenttools.Instrument)
        if not instrument:
            return False
        clef = note_or_chord._get_effective(indicatortools.Clef)
        if not clef:
            return False
        if clef == indicatortools.Clef(name='percussion'):
            if percussion_clef_is_allowed:
                return True
            else:
                return False
        if clef not in instrument.allowable_clefs:
            return False
    else:
        return True
