# -*- coding: utf-8 -*-
from abjad.tools.topleveltools import iterate


def list_pitches(expr):
    '''Lists pitches in `expr`.

    ..  container:: example

        **Example 1.** Lists named pitches in staff:

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> beam = spannertools.Beam()
            >>> attach(beam, staff[:])

        ::

            >>> for x in pitchtools.list_pitches(beam):
            ...     x
            ...
            NamedPitch("c'")
            NamedPitch("d'")
            NamedPitch("e'")
            NamedPitch("f'")

    Returns tuple.
    '''
    from abjad.tools import pitchtools
    from abjad.tools import scoretools
    from abjad.tools import spannertools

    if isinstance(expr, pitchtools.Pitch):
        result = pitchtools.NamedPitch.from_pitch_carrier(expr)
        return pitchtools.PitchSegment(
            items=(result,),
            item_class=pitchtools.NamedPitch,
            )
        
    result = []
    if hasattr(expr, 'written_pitches'):
        result.extend(expr.written_pitches)
    # for pitch arrays
    elif hasattr(expr, 'pitches'):
        result.extend(expr.pitches)
    elif isinstance(expr, spannertools.Spanner):
        for leaf in expr._get_leaves():
            if (hasattr(leaf, 'written_pitch') and
                not isinstance(leaf, scoretools.Rest)):
                result.append(leaf.written_pitch)
            elif hasattr(leaf, 'written_pitches'):
                result.extend(leaf.written_pitches)
    elif isinstance(expr, pitchtools.PitchSet):
        result.extend(sorted(list(expr)))
    elif isinstance(expr, (list, tuple, set)):
        for x in expr:
            result.extend(list_pitches(x))
    else:
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            if (hasattr(leaf, 'written_pitch') and
                not isinstance(leaf, scoretools.Rest)):
                result.append(leaf.written_pitch)
            elif hasattr(leaf, 'written_pitches'):
                result.extend(leaf.written_pitches)
    return pitchtools.PitchSegment(
        items=result,
        item_class=pitchtools.NamedPitch,
        )
