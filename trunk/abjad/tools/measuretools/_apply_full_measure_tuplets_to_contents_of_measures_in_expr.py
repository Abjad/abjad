import copy


# TODO: make public?
def _apply_full_measure_tuplets_to_contents_of_measures_in_expr(expr, supplement=None):
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
    from abjad.tools import iterationtools
    from abjad.tools import tuplettools

    for measure in iterationtools.iterate_measures_in_expr(expr):
        target_duration = measure.preprolated_duration
        tuplet = tuplettools.FixedDurationTuplet(target_duration, measure[:])
        if supplement:
            tuplet.extend(copy.deepcopy(supplement))
