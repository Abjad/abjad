from abjad.tools import durationtools


def copy_components_and_immediate_parent_of_first_component(components):
    r'''.. versionadded:: 1.1

    Copy `components` and immediate parent of first component.

    The `components` must be thread-contiguous.

    Return in newly created container equal to type of
    first element in `copmonents`.

    If the parent of the first element in `components` is a tuplet then
    insure that the tuplet multiplier of the function output
    equals the tuplet multiplier of the parent of the
    first element in `components`. ::

        >>> voice = Voice(r"\times 2/3 { c'8 d' e' } \times 2/3 { f'8 g' a' }")
        >>> voice.append(r"\times 2/3 { b'8 c'' d'' }")
        >>> beam = beamtools.BeamSpanner(voice.leaves[:4])

    ::

        >>> f(voice)
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8 ]
                g'8
                a'8
            }
            \times 2/3 {
                b'8
                c''8
                d''8
            }
        }

    ::

        >>> leaves = voice.leaves[:2]
        >>> componenttools.copy_components_and_immediate_parent_of_first_component(leaves)
        Tuplet(2/3, [c'8, d'8])

    Parent-contiguity is not required.
    Thread-contiguous `components` suffice. ::

        >>> leaves = voice.leaves[:5]
        >>> componenttools.copy_components_and_immediate_parent_of_first_component(leaves)
        Tuplet(2/3, [c'8, d'8, e'8, f'8, g'8])

    .. note:: this function copies only the *immediate parent* of
        the first element in `components`. This function ignores any further
        parentage of `components` above the immediate parent of `components`.

    .. todo:: this function should (but does not) copy marks that attach to `components` and
        to the immediate parent of the first component; extend function to do so.

    .. versionchanged:: 2.0
        renamed ``clonewp.with_parent()`` to
        ``componenttools.copy_components_and_immediate_parent_of_first_component()``.

    .. versionchanged:: 2.0
        renamed ``componenttools.clone_components_and_immediate_parent_of_first_component()`` to
        ``componenttools.copy_components_and_immediate_parent_of_first_component()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import contexttools
    from abjad.tools import measuretools

    # assert strictly contiguous components in same thread
    assert componenttools.all_are_thread_contiguous_components(components)

    # remember parent
    parent = components[0]._parent

    # new: remember parent multiplier, if any
    parent_multiplier = getattr(parent, 'multiplier', 1)

    # new: remember parent denominator, if any
    if isinstance(parent, measuretools.Measure):
        parent_denominator = contexttools.get_effective_time_signature(parent).denominator
    else:
        parent_denominator = None

    # remember parent's music
    parents_music = components[0]._parent._music

    # strip parent of music temporarily
    parent._music = []

    # copy parent without music
    result = componenttools.copy_components_and_fracture_crossing_spanners([parent])[0]

    # give music back to parent
    parent._music = parents_music

    new_components = componenttools.copy_components_and_fracture_crossing_spanners(components)

    result.extend(new_components)

    # TODO: change hard-coded class name testing to isinstance testing instead
    # new: resize result to match parent_multiplier, if resizable
    if result.__class__.__name__ == 'FixedDurationTuplet':
        result.target_duration = parent_multiplier * result.contents_duration
    elif result.__class__.__name__ == 'Measure':
        new_duration = parent_multiplier * result.contents_duration
        new_time_signature = contexttools.TimeSignatureMark(new_duration)
        contexttools.detach_time_signature_marks_attached_to_component(result)
        new_time_signature.attach(result)

    # new: rewrite result denominator, if available
    if parent_denominator is not None:
        old_meter = contexttools.get_effective_time_signature(result)
        old_meter_pair = (old_meter.numerator, old_meter.denominator)
        new_meter = durationtools.rational_to_duration_pair_with_specified_integer_denominator(
            old_meter_pair, parent_denominator)
        new_time_signature = contexttools.TimeSignatureMark(new_meter)
        contexttools.detach_time_signature_marks_attached_to_component(result)
        new_time_signature.attach(result)

    # return copy
    return result
