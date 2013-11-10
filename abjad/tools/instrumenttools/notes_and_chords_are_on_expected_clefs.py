# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import scoretools
from abjad.tools.topleveltools import iterate


def notes_and_chords_are_on_expected_clefs(
    expr, 
    percussion_clef_is_allowed=True,
    ):
    r'''True when notes and chords in `expr` are on expected clefs.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clef = marktools.Clef('treble')
        >>> attach(clef, staff)
        >>> violin = instrumenttools.Violin()
        >>> attach(violin, staff)

    ::

        >>> instrumenttools.notes_and_chords_are_on_expected_clefs(staff)
        True

    False otherwise:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clef = marktools.Clef('alto')
        >>> attach(clef, staff)
        >>> violin = instrumenttools.Violin()
        >>> attach(violin, staff)

    ::

        >>> instrumenttools.notes_and_chords_are_on_expected_clefs(staff)
        False

    Allows percussion clef when `percussion_clef_is_allowed` is true:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clef = marktools.Clef('percussion')
        >>> attach(clef, staff)
        >>> violin = instrumenttools.Violin()
        >>> attach(violin, staff)

    ..  doctest::

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

        >>> instrumenttools.notes_and_chords_are_on_expected_clefs(
        ...     staff, percussion_clef_is_allowed=True)
        True

    Disallows percussion clef when `percussion_clef_is_allowed` is false:

    ::

        >>> instrumenttools.notes_and_chords_are_on_expected_clefs(
        ...     staff, percussion_clef_is_allowed=False)
        False

    Returns boolean.
    '''
    from abjad.tools import instrumenttools
    for note_or_chord in iterate(expr).by_class(
        (scoretools.Note, scoretools.Chord)):
        instrument = note_or_chord._get_effective_context_mark(
            instrumenttools.Instrument)
        if not instrument:
            return False
        clef = note_or_chord._get_effective_context_mark(marktools.Clef)
        if not clef:
            return False
        if clef == marktools.Clef('percussion'):
            if percussion_clef_is_allowed:
                return True
            else:
                return False
        if clef not in instrument.allowable_clefs:
            return False
    else:
        return True
