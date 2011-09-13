from abjad.tools import sequencetools
from abjad.tools.pitchtools.MelodicChromaticIntervalSegment import MelodicChromaticIntervalSegment
from abjad.tools.pitchtools.calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier import calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier
from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


def expr_to_melodic_chromatic_interval_segment(expr):
    '''.. versionadded:: 2.0

    Change `expr` to melodic chromatic interval segment::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        abjad> pitchtools.expr_to_melodic_chromatic_interval_segment(staff)
        MelodicChromaticIntervalSegment(+2, +2, +1, +2, +2, +2, +1)

    Return melodic chromatic interval segment.
    '''

    pitches = list_named_chromatic_pitches_in_expr(expr)
    mcis = []
    for left, right in sequencetools.iterate_sequence_pairwise_strict(pitches):
        mci = calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(left, right)
        mcis.append(mci)

    return MelodicChromaticIntervalSegment(mcis)
