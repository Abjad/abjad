from abjad.tools import pitchtools


def analyze_chord(expr):
    '''Analyze `expr` and return chord class:

    ::

        >>> chord = Chord([7, 10, 12, 16], (1, 4))
        >>> tonalanalysistools.analyze_chord(chord)
        CDominantSeventhInSecondInversion

    Return none when no tonal chord is understood:

    ::

        >>> chord = Chord(['c', 'cs', 'd'], (1, 4))
        >>> tonalanalysistools.analyze_chord(chord) is None
        True

    Raise tonal harmony error when chord can not analyze.
    '''
    from abjad.tools import tonalanalysistools
    from abjad.tools.tonalanalysistools import ChordQualityIndicator as CQI

    pitches = pitchtools.list_named_chromatic_pitches_in_expr(expr)
    npcset = pitchtools.NamedChromaticPitchClassSet(pitches)

    ordered_npcs = []
    letters = ('c', 'e', 'g', 'b', 'd', 'f', 'a')
    for letter in letters:
        for npc in npcset:
            if npc._diatonic_pitch_class_name == letter:
                ordered_npcs.append(npc)

    ordered_npcs = pitchtools.NamedChromaticPitchClassSegment(ordered_npcs)
    for x in range(len(ordered_npcs)):
        ordered_npcs = ordered_npcs.rotate(1)
        segment = \
            ordered_npcs.inversion_equivalent_diatonic_interval_class_segment
        if segment.is_tertian:
            break
    else:
        return None

    root = ordered_npcs[0]
    indicator = CQI.from_diatonic_interval_class_segment(segment)
    bass = min(pitches).named_chromatic_pitch_class
    inversion = ordered_npcs.index(bass)

    return tonalanalysistools.ChordClass(
        root,
        indicator.quality_string,
        indicator.extent,
        inversion,
        )
