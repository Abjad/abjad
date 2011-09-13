from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


# TODO: rename to apply_octavation_spanner_to_pitched_components_in_expr
def apply_octavation_spanner_to_pitched_components(expr,
    ottava_numbered_diatonic_pitch = None, quindecisima_numbered_diatonic_pitch = None):
    r""".. versionadded:: 1.1

    Apply octavation spanner to pitched components in `expr`::

        abjad> t = Measure((4, 8), notetools.make_notes([24, 26, 27, 29], [(1, 8)]))
        abjad> pitchtools.apply_octavation_spanner_to_pitched_components(t, ottava_numbered_diatonic_pitch = 14)
        OctavationSpanner(|4/8(4)|)

    ::

        abjad> print t.format
            {
                \time 4/8
                \ottava #1
                c'''8
                d'''8
                ef'''8
                f'''8
                \ottava #0
            }

    Apply octavation spanner according to the diatonic pitch number of
    the maximum pitch in `expr`.

    Return octavation spanner.
    """
    from abjad.tools.spannertools import OctavationSpanner

    pitches = list_named_chromatic_pitches_in_expr(expr)
    max_pitch = max(pitches)
    max_numbered_diatonic_pitch = max_pitch.numbered_diatonic_pitch

    if ottava_numbered_diatonic_pitch is not None:
        if ottava_numbered_diatonic_pitch <= max_numbered_diatonic_pitch:
            octavation = OctavationSpanner(expr)
            octavation.start = 1
            if quindecisima_numbered_diatonic_pitch is not None:
                if quindecisima_numbered_diatonic_pitch <= max_numbered_diatonic_pitch:
                    octavation.start = 2
            #else:
            #   octavation.start = 1

    try:
        return octavation
    except NameError:
        return None
