# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import iterationtools


def notes_and_chords_are_on_expected_clefs(
    expr, 
    percussion_clef_is_allowed=True,
    ):
    r'''True when notes and chords in `expr` are on expected clefs.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.ClefMark('treble')(staff)
        ClefMark('treble')(Staff{4})
        >>> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

    ::

        >>> instrumenttools.notes_and_chords_are_on_expected_clefs(staff)
        True

    False otherwise:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.ClefMark('alto')(staff)
        ClefMark('alto')(Staff{4})
        >>> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

    ::

        >>> instrumenttools.notes_and_chords_are_on_expected_clefs(staff)
        False

    Allows percussion clef when `percussion_clef_is_allowed` is true:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.ClefMark('percussion')(staff)
        ClefMark('percussion')(Staff{4})
        >>> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

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

    for note_or_chord in iterationtools.iterate_notes_and_chords_in_expr(expr):
        instrument = note_or_chord._get_effective_context_mark(
            instrumenttools.Instrument)
        if not instrument:
            return False
        clef = note_or_chord._get_effective_context_mark(contexttools.ClefMark)
        if not clef:
            return False
        if clef == contexttools.ClefMark('percussion'):
            if percussion_clef_is_allowed:
                return True
            else:
                return False
        if clef not in instrument.allowable_clefs:
            return False
    else:
        return True
