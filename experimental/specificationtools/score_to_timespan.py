def score_to_timespan(score=None):
    r'''.. versionadded:: 1.0

    Change optional `score` to timespan::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.score_to_timespan()
        Timespan(ComponentSelector())

    Return timespan.
    '''
    from experimental import specificationtools
    
    # check input
    if score is None:
        score_name = None
    else:
        score_name = specificationtools.expr_to_score_name(score)

    # make score indicator
    score_indicator = specificationtools.ComponentSelector()

    # return timespan
    return score_indicator.timespan
