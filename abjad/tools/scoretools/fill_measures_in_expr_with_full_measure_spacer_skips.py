# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def fill_measures_in_expr_with_full_measure_spacer_skips(expr, iterctrl=None):
    r'''Fill measures in `expr` with full-measure spacer skips.
    '''
    from abjad.tools import scoretools

    if iterctrl is None:
        iterctrl = lambda measure, i: True

    measures = iterate(expr).by_class(scoretools.Measure)
    for i, measure in enumerate(measures):
        if iterctrl(measure, i):
            skip = scoretools.Skip(1)
            # allow zero-update iteration
            time_signature = measure.time_signature
            duration = time_signature.duration
            if measure.implicit_scaling:
                implied_prolation = time_signature.implied_prolation
                multiplier = duration.__div__(implied_prolation)
            else:
                multiplier = durationtools.Multiplier(duration)
            attach(multiplier, skip)
            measure[:] = [skip]
            for spanner in measure._get_spanners():
                spanner._remove(measure)
