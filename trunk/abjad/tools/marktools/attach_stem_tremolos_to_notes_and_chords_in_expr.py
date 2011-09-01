from abjad.tools.marktools.StemTremolo import StemTremolo


def attach_stem_tremolos_to_notes_and_chords_in_expr(expr, stem_tremolos):
    r'''.. versionadded:: 2.3

    Attach `stem_tremolos` to notes and chords in `expr`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> stem_tremolo = marktools.StemTremolo(16)
        abjad> marktools.attach_stem_tremolos_to_notes_and_chords_in_expr(staff, [stem_tremolo])

    ::

        abjad> f(staff)
        \new Staff {
            c'8 :16
            d'8 :16
            e'8 :16
            f'8 :16
        }

    Return none.
    '''
    from abjad.tools import leaftools

    for note_or_chord in leaftools.iterate_notes_and_chords_forward_in_expr(expr):
        for stem_tremolo in stem_tremolos:
            StemTremolo(stem_tremolo)(note_or_chord)
