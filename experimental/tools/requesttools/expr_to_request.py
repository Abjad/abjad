import copy


def expr_to_request(expr):
    r'''.. versionadded:: 1.0

    Change request `expr` to request object.

    If `expr` is one of ... ::

        Request
        StatalServer
        Handler
        built-in
        
    ... then return ... ::

        Request
        StatalServerRequest
        HandlerRequest
        AbsoluteRequest

    ... as output.
    '''
    from abjad.tools import rhythmmakertools
    from experimental.tools import handlertools
    from experimental.tools import requesttools
    from experimental.tools import statalservertools
    from experimental.tools import timeexpressiontools

    # probably precautionary: prune expr of any incoming references
    expr = copy.deepcopy(expr)

    if isinstance(expr, requesttools.Request):
        return expr
    elif isinstance(expr, statalservertools.StatalServer):
        return requesttools.StatalServerRequest(expr)
    elif isinstance(expr, handlertools.Handler):
        return requesttool.HandlerRequest(expr)
    elif isinstance(expr, (tuple, list, str, rhythmmakertools.RhythmMaker)):
        return requesttools.AbsoluteRequest(expr)
    elif isinstance(expr, timeexpressiontools.TimespanExpression):
        return expr
    else:
        raise TypeError('do not know how to change {!r} to request object.'.format(expr))
