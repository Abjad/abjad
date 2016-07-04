# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import iterate


def notes_and_chords_are_on_expected_clefs(
    expr,
    percussion_clef_is_allowed=True,
    ):
    r'''Is true when notes and chords in `expr` are on expected clefs.

    ..  todo:: Move to WellformednessManager.

    ..  container:: example

        **Example 1.** Expected clef:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> clef = Clef(name='treble')
            >>> attach(clef, staff)
            >>> violin = instrumenttools.Violin()
            >>> attach(violin, staff)
            >>> show(staff) # doctest: +SKIP

        ::

            >>> instrumenttools.notes_and_chords_are_on_expected_clefs(staff)
            True

    ..  container:: example

        **Example 2.** Unexpected clef:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> clef = Clef(name='alto')
            >>> attach(clef, staff)
            >>> violin = instrumenttools.Violin()
            >>> attach(violin, staff)
            >>> show(staff) # doctest: +SKIP

        ::

            >>> instrumenttools.notes_and_chords_are_on_expected_clefs(staff)
            False

    ..  container:: example

        **Example 3.** Allows percussion clef:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> clef = Clef(name='percussion')
            >>> attach(clef, staff)
            >>> violin = instrumenttools.Violin()
            >>> attach(violin, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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

            >>> instrumenttools.notes_and_chords_are_on_expected_clefs(
            ...     staff, percussion_clef_is_allowed=True)
            True

    ..  container:: example

        **Example 4.** Forbids percussion clef:

        ::

            >>> instrumenttools.notes_and_chords_are_on_expected_clefs(
            ...     staff, percussion_clef_is_allowed=False)
            False

    Returns true or false.
    '''
    from abjad.tools import instrumenttools
    prototype = (scoretools.Note, scoretools.Chord)
    for note_or_chord in iterate(expr).by_class(prototype):
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