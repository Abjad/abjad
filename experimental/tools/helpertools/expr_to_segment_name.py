def expr_to_segment_name(expr):
    r'''
    
    Change segment specification to segment name::

        >>> from experimental.tools import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')


    ::

        >>> red_segment
        SegmentSettingInterface('red')

    ::

        >>> helpertools.expr_to_segment_name(red_segment)
        'red'

    Leave string unchanged::

        >>> helpertools.expr_to_segment_name('red')
        'red'

    Raise exception on nonsegment, nonstring input.

    Return string.
    '''
    from experimental.tools import specificationtools
    from experimental.tools import settingtools
    if isinstance(expr, specificationtools.SegmentSpecification):
        return expr.segment_name
    if isinstance(expr, settingtools.SegmentSettingInterface):
        return expr.segment_name
    elif isinstance(expr, str):
        return expr
    else:
        raise Exception('{!r} is neither segment nor string.'.format(expr))
