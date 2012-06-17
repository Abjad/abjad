def expr_to_score_name(expr):
    r'''.. versionadded:: 1.0

    Change `expr` to score name.

    Allow `expr` equal score object, score specification,
    segment specification or score name.

    Return string.
    '''
    from abjad.tools import scoretools
    from experimental import specificationtools

    if isinstance(expr, str):
        score_name = expr
    elif isinstance(expr, scoretools.Score):
        score_name = expr.name
    elif isinstance(expr, specificationtools.Specification):
        score_name = expr.score_name
    else:
        raise Exception('{!r} is neither string nor score nor specification.')

    return score_name
