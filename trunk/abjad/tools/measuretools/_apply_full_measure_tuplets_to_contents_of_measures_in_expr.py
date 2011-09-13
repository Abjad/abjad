from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr
import copy


def _apply_full_measure_tuplets_to_contents_of_measures_in_expr(expr, supplement = None):
    '''Tupletize the contents of every measure in expr.
    When supplement is not None, extend newly created
    FixedDurationTuplet by copy of supplement.

    Use primarily during rhythmic construction.

    Note that supplement should be a Python list of
    notes, rests, chords, tuplets or whatever.

    .. versionchanged:: 2.0
        renamed ``measuretools.tupletize()``
        to ``measuretools._apply_full_measure_tuplets_to_contents_of_measures_in_expr()``.
    '''
    from abjad.tools.tuplettools.FixedDurationTuplet import FixedDurationTuplet

    for measure in iterate_measures_forward_in_expr(expr):
        target_duration = measure.preprolated_duration
        tuplet = FixedDurationTuplet(target_duration, measure[:])
        if supplement:
            tuplet.extend(copy.deepcopy(supplement))
