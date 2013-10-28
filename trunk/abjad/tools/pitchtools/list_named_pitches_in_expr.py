# -*- encoding: utf-8 -*-


def list_named_pitches_in_expr(expr):
    '''List named pitches in `expr`:

    ::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> beam = spannertools.BeamSpanner()
        >>> attach(beam, staff[:])

    ::

        >>> for x in pitchtools.list_named_pitches_in_expr(beam):
        ...     x
        ...
        NamedPitch("c'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("f'")

    Returns tuple.
    '''
    from abjad.tools import spannertools
    from abjad.tools import iterationtools
    from abjad.tools import leaftools
    from abjad.tools import pitchtools
    from abjad.tools import resttools

    # TODO: remove try-except
    try:
        result = pitchtools.get_named_pitch_from_pitch_carrier(expr)
        return pitchtools.PitchSegment(
            tokens=(result,),
            item_class=pitchtools.NamedPitch,
            )
    except (TypeError, MissingPitchError, ExtraPitchError):
        result = []
        if hasattr(expr, 'written_pitches'):
            result.extend(expr.written_pitches)
        # for pitch arrays
        elif hasattr(expr, 'pitches'):
            result.extend(expr.pitches)
        elif isinstance(expr, spannertools.Spanner):
            for leaf in expr.leaves:
                if hasattr(leaf, 'written_pitch') and not isinstance(leaf, resttools.Rest):
                    result.append(leaf.written_pitch)
                elif hasattr(leaf, 'written_pitches'):
                    result.extend(leaf.written_pitches)
        elif isinstance(expr, pitchtools.PitchSet):
            result.extend(sorted(list(expr)))
        elif isinstance(expr, (list, tuple, set)):
            for x in expr:
                result.extend(list_named_pitches_in_expr(x))
        else:
            for leaf in iterationtools.iterate_leaves_in_expr(expr):
                if hasattr(leaf, 'written_pitch') and not isinstance(leaf, resttools.Rest):
                    result.append(leaf.written_pitch)
                elif hasattr(leaf, 'written_pitches'):
                    result.extend(leaf.written_pitches)
        return pitchtools.PitchSegment(
            tokens=result,
            item_class=pitchtools.NamedPitch,
            )
