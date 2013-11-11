# -*- encoding: utf-8 -*-
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import attach


def fill_measures_in_expr_with_full_measure_spacer_skips(expr, iterctrl=None):
    r'''Fill measures in `expr` with full-measure spacer skips.
    '''
    from abjad.tools import scoretools

    if iterctrl is None:
        iterctrl = lambda measure, i: True

    for i, measure in enumerate(iterate(expr).by_class(scoretools.Measure)):
        if iterctrl(measure, i):
            skip = scoretools.Skip(1)
            # allow zero-update iteration
            time_signature = measure.time_signature
            #skip.lilypond_duration_multiplier = \
            #    time_signature.duration / time_signature.implied_prolation
            multiplier = time_signature.duration / time_signature.implied_prolation
            attach(multiplier, skip)
            measure[:] = [skip]
            for spanner in measure._get_spanners():
                spanner._remove(measure)
