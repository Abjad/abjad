import copy
from experimental import helpertools


def source_to_request(source, callback=None, count=None, offset=None, reverse=None):
    r'''.. versionadded:: 1.0

    Change request `source` to request object.

    If `source` is one of ... ::

        StatalServer Handler

    ... then return ... ::

        StatalServerRequest
        HandlerRequest

    ... as output.

    If `source` is a constant then return `source` unchanged.

    If `source` is already a request then set `callback`, `count`, `offset`
    or `reverse` against `source` (if any are not none) and return `source`.
    '''
    from experimental import handlertools
    from experimental import requesttools
    from experimental import statalservertools

    assert isinstance(callback, (helpertools.Callback, type(None))), repr(callback)
    assert isinstance(count, (int, type(None))), repr(count)
    assert isinstance(offset, (int, type(None))), repr(offset)

    if isinstance(source, requesttools.Request):
        request = copy.copy(source)
        if callback is not None:
            request.callback = callback
        if count is not None:
            request.count = count
        if offset is not None:
            request.offset = offset
        if reverse is not None:
            request.reverse = reverse
    elif isinstance(source, statalservertools.StatalServer):
        if count is not None or offset is not None or reverse is not None:
            request = requesttools.StatalServerRequest(
                source, count=count, offset=offset, reverse=reverse)
    elif isinstance(source, handlertools.Handler):
        if offset is not None:
            assert count is None
            request = requesttools.HandlerRequest(source, offset=offset)
    elif any([x is not None for x in (callback, count, offset, reverse)]):
        raise ValueError(
            "'callback', 'count', 'offset' or 'reverse' set on stateless source: {!r}.".format(source))
    else:
        request = source

    return request
