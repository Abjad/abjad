# -*- encoding: utf-8 -*-


def fill_measures_in_expr_with_full_measure_spacer_skips(expr, iterctrl=None):
    '''Fill measures in `expr` with full-measure spacer skips.
    '''
    from abjad.tools import scoretools
    from abjad.tools.topleveltools import iterate

    if iterctrl is None:
        iterctrl = lambda measure, i: True

    for i, measure in enumerate(iterate(expr).by_class(scoretools.Measure)):
        if iterctrl(measure, i):
            skip = scoretools.Skip(1)
            # allow zero-update iteration
            time_signature = measure.time_signature
            skip.lilypond_duration_multiplier = \
                time_signature.duration / time_signature.implied_prolation
            measure[:] = [skip]
            for spanner in measure._get_spanners():
                spanner._remove(measure)
