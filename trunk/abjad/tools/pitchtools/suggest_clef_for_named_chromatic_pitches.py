from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


# TODO: renamed to suggest_clef_for_named_chromatic_pitches_in_expr
def suggest_clef_for_named_chromatic_pitches(pitches):
    '''.. versionadded:: 1.1

    Suggest clef for named chromatic `pitches`::

        abjad> staff = Staff(notetools.make_notes(range(-12, -6), [(1, 4)]))
        abjad> pitchtools.suggest_clef_for_named_chromatic_pitches(staff)
        ClefMark('bass')

    Suggest clef based on minimal number of ledger lines.

    Return clef mark.

    .. versionchanged:: 2.0
        renamed ``pitchtools.suggest_clef()`` to
        ``pitchtools.suggest_clef_for_named_chromatic_pitches()``.
    '''
    from abjad.tools import contexttools

    pitches = list_named_chromatic_pitches_in_expr(pitches)

    diatonic_pitch_numbers = [abs(pitch.numbered_diatonic_pitch) for pitch in pitches]
    max_diatonic_pitch_number = max(diatonic_pitch_numbers)
    min_diatonic_pitch_number = min(diatonic_pitch_numbers)

    lowest_treble_line_pitch = NamedChromaticPitch('e', 4)
    lowest_treble_line_diatonic_pitch_number = \
        abs(lowest_treble_line_pitch.numbered_diatonic_pitch)
    candidate_steps_below_treble = \
        lowest_treble_line_diatonic_pitch_number - min_diatonic_pitch_number

    highest_bass_line_pitch = NamedChromaticPitch('a', 3)
    highest_bass_line_diatonic_pitch_number = \
        abs(highest_bass_line_pitch.numbered_diatonic_pitch)
    candidate_steps_above_bass = max_diatonic_pitch_number - highest_bass_line_diatonic_pitch_number

    if candidate_steps_above_bass < candidate_steps_below_treble:
        return contexttools.ClefMark('bass')
    else:
        return contexttools.ClefMark('treble')
