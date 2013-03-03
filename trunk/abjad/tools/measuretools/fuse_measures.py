from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools


def fuse_measures(measures):
    r'''.. versionadded:: 1.1

    Fuse `measures`::

        >>> staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(
        ...     [(1, 8), (2, 16)]))
        >>> measuretools.fill_measures_in_expr_with_repeated_notes(staff, Duration(1, 16))
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
        >>> beamtools.BeamSpanner(staff.leaves)
        BeamSpanner(c'16, d'16, e'16, f'16)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 1/8
                c'16 [
                d'16
            }
            {
                \time 2/16
                e'16
                f'16 ]
            }
        }

    ::

        >>> measuretools.fuse_measures(staff[:])
        Measure(2/8, [c'16, d'16, e'16, f'16])

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'16 [
                d'16
                e'16
                f'16 ]
            }
        }

    Return new measure.

    Allow parent-contiguous `measures`.

    Allow outside-of-score `measures`.

    Do not define measure fusion across intervening container boundaries.

    Calculate best new time signature.

    Instantiate new measure.

    Give `measures` contents to new measure.

    Give `measures` dominant spanners to new measure.

    Give `measures` parentage to new measure.

    Leave `measures` empty, unspanned and outside-of-score.
    '''
    from abjad.tools import contexttools
    from abjad.tools import measuretools
    from abjad.tools import timesignaturetools
    from abjad.tools.componenttools._switch_components_to_parent import _switch_components_to_parent
    from abjad.tools.spannertools._give_spanners_that_dominate_donor_components_to_recipient_components \
        import _give_spanners_that_dominate_donor_components_to_recipient_components

    assert componenttools.all_are_contiguous_components_in_same_parent(measures,
        klasses=(measuretools.Measure, ))

    if len(measures) == 0:
        return None

    # TODO: Instantiate a new measure, even length is 1 #

    if len(measures) == 1:
        return measures[0]

    parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components(measures)

    old_denominators = []
    new_duration = durationtools.Duration(0)
    for measure in measures:
        effective_time_signature = contexttools.get_effective_time_signature(measure)
        old_denominators.append(effective_time_signature.denominator)
        new_duration += effective_time_signature.duration

    new_time_signature = timesignaturetools.duration_and_possible_denominators_to_time_signature(
        new_duration, old_denominators)

    music = []
    for measure in measures:
        # scale before reassignment to prevent tie chain scale drama
        multiplier = \
            contexttools.get_effective_time_signature(measure).implied_prolation / \
            new_time_signature.implied_prolation
        containertools.scale_contents_of_container(measure, multiplier)
        measure_music = measure[:]
        _switch_components_to_parent(measure_music, None)
        music += measure_music

    new_measure = measuretools.Measure(new_time_signature, music)

    if parent is not None:
        _give_spanners_that_dominate_donor_components_to_recipient_components(measures, [new_measure])

    _switch_components_to_parent(measures, None)
    if parent is not None:
        parent.insert(start, new_measure)

    return new_measure
