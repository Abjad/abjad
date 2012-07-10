def expr_to_segment_name(expr):
    r'''.. versionadded:: 1.0
    
    Change segment specification to segment name::

        >>> from abjad.tools import scoretemplatetools
        >>> from experimental import selectortools
        >>> from experimental import specificationtools

    ::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1)
        >>> segment = specificationtools.SegmentSpecification(template, 'red')

    ::

        >>> segment
        SegmentSpecification('red')

    ::

        >>> selectortools.expr_to_segment_name(segment)
        'red'

    Leave string unchanged::

        >>> selectortools.expr_to_segment_name('red')
        'red'

    Raise exception on nonsegment, nonstring input.

    Return string.
    '''
    from experimental import specificationtools
    if isinstance(expr, specificationtools.SegmentSpecification):
        return expr.name
    elif isinstance(expr, str):
        return expr
    else:
        raise Exception('{!r} is neither segment nor string.'.format(expr))
