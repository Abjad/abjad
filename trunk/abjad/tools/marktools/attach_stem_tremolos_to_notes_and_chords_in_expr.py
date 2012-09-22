def attach_stem_tremolos_to_notes_and_chords_in_expr(expr, stem_tremolos):
    r'''.. versionadded:: 2.3

    Attach `stem_tremolos` to notes and chords in `expr`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> stem_tremolo = marktools.StemTremolo(16)
        >>> marktools.attach_stem_tremolos_to_notes_and_chords_in_expr(staff, [stem_tremolo])

    ::

        >>> f(staff)
        \new Staff {
            c'8 :16
            d'8 :16
            e'8 :16
            f'8 :16
        }

    Return none.
    '''
    # TODO: marktools should be able to import leaftools at top level
    from abjad.tools import iterationtools
    from abjad.tools import marktools

    for note_or_chord in iterationtools.iterate_notes_and_chords_in_expr(expr):
        for stem_tremolo in stem_tremolos:
            marktools.StemTremolo(stem_tremolo)(note_or_chord)
