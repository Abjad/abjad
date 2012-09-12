import copy
from experimental import helpertools


# NEXT TODO: remove transform keywords
def expr_to_request(expr, index=None, count=None, reverse=None, rotation=None, callback=None):
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

    Set any of `index`, `count`, `reverse`, `rotation` or 
    `callback` that are not none against request
    and return request.
    '''
    from experimental import handlertools
    from experimental import requesttools
    from experimental import statalservertools

    expr = copy.deepcopy(expr)

    if isinstance(expr, requesttools.Request):
        request = expr
    elif isinstance(expr, statalservertools.StatalServer):
        request = requesttools.StatalServerRequest(expr)
    elif isinstance(expr, handlertools.Handler):
        request = requesttool.HandlerRequest(expr)
    else:
        request = requesttools.AbsoluteRequest(expr)

    requesttools.set_transforms_on_request(
        request, index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    return request
