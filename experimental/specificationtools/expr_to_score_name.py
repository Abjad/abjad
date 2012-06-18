def expr_to_score_name(expr):
    r'''.. versionadded:: 1.0
    
    Change score specification to score specification name::

        >>> from experimental import specificationtools

    ::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1)
        >>> score_specification = specificationtools.ScoreSpecification(template)

    ::

        >>> specificationtools.expr_to_score_name(score_specification)
        'Grouped Rhythmic Staves Score'

    Change score to score name::

        >>> score = scoretools.Score([], name='Colored Score')

    ::

        >>> specificationtools.expr_to_score_name(score)
        'Colored Score'

    Leave string unchanged::

        >>> specificationtools.expr_to_score_name('Colored Score')
        'Colored Score'

    Raise exception on nonscore specification, nonscore, nonstring input.

    Return string.
    '''
    from abjad.tools import scoretools
    from experimental import specificationtools

    if isinstance(expr, specificationtools.ScoreSpecification):
        return expr.name
    if isinstance(expr, scoretools.Score):
        return expr.name
    elif isinstance(expr, str):
        return expr
    else:
        raise Exception('{!r} is neither score specification nor score nor string.'.format(expr))
