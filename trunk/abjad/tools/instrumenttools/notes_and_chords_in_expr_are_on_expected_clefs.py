from abjad.tools import contexttools
from abjad.tools.contexttools.get_effective_instrument import get_effective_instrument


def notes_and_chords_in_expr_are_on_expected_clefs(expr, percussion_clef_is_allowed = True):
    r'''.. versionadded:: 2.0

    True when notes and chords in `expr` are on expected clefs::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('treble')(staff)
        ClefMark('treble')(Staff{4})
        abjad> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

    ::

        abjad> instrumenttools.notes_and_chords_in_expr_are_on_expected_clefs(staff)
        True

    False otherwise::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('alto')(staff)
        ClefMark('alto')(Staff{4})
        abjad> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

    ::

        abjad> instrumenttools.notes_and_chords_in_expr_are_on_expected_clefs(staff)
        False

    Allow percussion clef when `percussion_clef_is_allowed` is true::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('percussion')(staff)
        ClefMark('percussion')(Staff{4})
        abjad> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

    ::

        abjad> f(staff)
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

        abjad> instrumenttools.notes_and_chords_in_expr_are_on_expected_clefs(staff, percussion_clef_is_allowed = True)
        True

    Disallow percussion clef when `percussion_clef_is_allowed` is false::

        abjad> instrumenttools.notes_and_chords_in_expr_are_on_expected_clefs(staff, percussion_clef_is_allowed = False)
        False

    Return boolean.
    '''
    from abjad.tools import leaftools

    for note_or_chord in leaftools.iterate_notes_and_chords_forward_in_expr(expr):
        instrument = get_effective_instrument(note_or_chord)
        if not instrument:
            return False
        clef = contexttools.get_effective_clef(note_or_chord)
        if not clef:
            return False
        if clef == contexttools.ClefMark('percussion'):
            if percussion_clef_is_allowed:
                return True
            else:
                return False
        if clef not in instrument.all_clefs:
            return False
    else:
        return True
