from abjad.exceptions import ExtraPitchError
from abjad.exceptions import MissingPitchError
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import get_named_chromatic_pitch_from_pitch_carrier


def list_named_chromatic_pitches_in_expr(expr):
    '''.. versionadded:: 2.0

    List named chromatic pitches in `expr`::

        abjad> t = Staff("c'4 d'4 e'4 f'4")
        abjad> beam = spannertools.BeamSpanner(t[:])
        abjad> pitchtools.list_named_chromatic_pitches_in_expr(beam)
        (NamedChromaticPitch("c'"), NamedChromaticPitch("d'"), NamedChromaticPitch("e'"), NamedChromaticPitch("f'"))

    Return tuple.
    '''
    from abjad.tools.spannertools import Spanner
    from abjad.tools.resttools.Rest import Rest
    from abjad.tools import leaftools
    from abjad.tools.pitchtools.NamedChromaticPitchSet import NamedChromaticPitchSet

    try:
        result = get_named_chromatic_pitch_from_pitch_carrier(expr)
        return (result, )
    except (TypeError, MissingPitchError, ExtraPitchError):
        result = []
        if hasattr(expr, 'written_pitches'):
            result.extend(expr.written_pitches)
        # for pitch arrays
        elif hasattr(expr, 'pitches'):
            result.extend(expr.pitches)
        elif isinstance(expr, Spanner):
            for leaf in expr.leaves:
                if hasattr(leaf, 'written_pitch') and not isinstance(leaf, Rest):
                    result.append(leaf.written_pitch)
                elif hasattr(leaf, 'written_pitches'):
                    result.extend(leaf.written_pitches)
        elif isinstance(expr, NamedChromaticPitchSet):
            pitches = list(expr)
            pitches.sort()
            pitches = tuple(pitches)
            return pitches
        elif isinstance(expr, (list, tuple, set)):
            for x in expr:
                result.extend(list_named_chromatic_pitches_in_expr(x))
        else:
            for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
                if hasattr(leaf, 'written_pitch') and not isinstance(leaf, Rest):
                    result.append(leaf.written_pitch)
                elif hasattr(leaf, 'written_pitches'):
                    result.extend(leaf.written_pitches)
        return tuple(result)
