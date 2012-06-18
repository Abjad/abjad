def make_score_measure_indicator(start_measure_number=None, stop_measure_number=None):
    r'''.. versionadded:: 1.0

    Make score slice indicator for measures from `start_measure_number`
    to `stop_measure_number`.

    The input parameters work like indices passed to built-in ``slice()``.

    Return score slice indicator.

    .. note:: it's possible that this function should really be a selection
        function. The name would be select_meaures_from_score() and the
        function would be paired with select_measures_from_context(). But
        those can probably both be generalized by select_measures() with
        an optional 'context' keyword.
    '''
    from abjad.tools import measuretools
    from experimental import specificationtools
    
    # TODO: implement me
