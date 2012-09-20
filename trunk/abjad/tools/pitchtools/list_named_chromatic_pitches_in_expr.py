def list_named_chromatic_pitches_in_expr(expr):
    '''.. versionadded:: 2.0

    List named chromatic pitches in `expr`::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> beam_spanner = beamtools.BeamSpanner(staff[:])

    ::

        >>> for x in pitchtools.list_named_chromatic_pitches_in_expr(beam_spanner):
        ...     x
        ...
        NamedChromaticPitch("c'")
        NamedChromaticPitch("d'")
        NamedChromaticPitch("e'")
        NamedChromaticPitch("f'")

    Return tuple.
    '''
    from abjad.tools import spannertools
    from abjad.tools import iterationtools
    from abjad.tools import leaftools
    from abjad.tools import pitchtools
    from abjad.tools import resttools

    # TODO: remove try-except
    try:
        result = pitchtools.get_named_chromatic_pitch_from_pitch_carrier(expr)
        return (result, )
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
        elif isinstance(expr, pitchtools.NamedChromaticPitchSet):
            pitches = list(expr)
            pitches.sort()
            pitches = tuple(pitches)
            return pitches
        elif isinstance(expr, (list, tuple, set)):
            for x in expr:
                result.extend(list_named_chromatic_pitches_in_expr(x))
        else:
            for leaf in iterationtools.iterate_leaves_in_expr(expr):
                if hasattr(leaf, 'written_pitch') and not isinstance(leaf, resttools.Rest):
                    result.append(leaf.written_pitch)
                elif hasattr(leaf, 'written_pitches'):
                    result.extend(leaf.written_pitches)
        return tuple(result)
