from abjad.tools import componenttools


# TODO: Finish implementation #

def _overdraw(expr, source_count = 1, total_reps = 2):
    '''Input parameters:

    source_count gives the number of measures to copy.
    total_reps gives the number of times source_count should repeat.

    Iterate expr. Copy the first source_count measures as 'source'.
    'Draw', or paste, source 'over' the following measures in expr
    a total of total_reps times.

    Return a Python list of multiplied source measures.

    Example:
    '''

    source = []
    result = []
    for i, measure in enumerate(measuretools.iterate_measures_forward_in_expr(expr)):
        if i < source_count:
            source.append(measure)
        elif i == source_count:
            componenttools.copy_components_and_fracture_crossing_spanners(source)
        else:
            pass
