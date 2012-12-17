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
    from experimental import handlertools
    from experimental import requesttools
    from experimental import statalservertools

    # TODO: maybe this line is safe to remove
    #expr = copy.deepcopy(expr)

    if isinstance(expr, requesttools.Request):
        return expr
    elif isinstance(expr, statalservertools.StatalServer):
        return requesttools.StatalServerRequest(expr)
    elif isinstance(expr, handlertools.Handler):
        return requesttool.HandlerRequest(expr)
    else:
        return requesttools.AbsoluteRequest(expr)
