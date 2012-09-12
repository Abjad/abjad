import copy
from experimental import helpertools


def source_to_request(source, index=None, count=None, reverse=None, rotation=None, callback=None):
    r'''.. versionadded:: 1.0

    Change request `source` to request object.

    If `source` is one of ... ::

        StatalServer Handler

    ... then return ... ::

        StatalServerRequest
        HandlerRequest

    ... as output.

    If `source` is a constant then return `source` unchanged.

    If `source` is already a request then set `index`, `count`, 
    `reverse`, `rotation` or `callback` against `source` 
    (if any are not none) and return `source`.
    '''
    from experimental import handlertools
    from experimental import requesttools
    from experimental import statalservertools

    assert isinstance(index, (int, type(None))), repr(index)
    assert isinstance(count, (int, type(None))), repr(count)
    assert isinstance(reverse, (bool, type(None))), repr(count)
    assert isinstance(rotation, (int, type(None))), repr(count)
    assert isinstance(callback, (helpertools.Callback, type(None))), repr(callback)

    if isinstance(source, requesttools.Request):
        request = copy.copy(source)
        if index is not None:
            request._index = index
        if count is not None:
            request._count = count
        if reverse is not None:
            request._reverse = reverse
        if rotation is not None:
            request._rotation = rotation
        if callback is not None:
            request._callback = callback
    elif isinstance(source, statalservertools.StatalServer):
        if count is not None or index is not None or reverse is not None or rotation is not None:
            request = requesttools.StatalServerRequest(
                source, count=count, index=index, reverse=reverse, rotation=rotation)
    elif isinstance(source, handlertools.Handler):
        if index is not None:
            assert count is None
            request = requesttools.HandlerRequest(source, index=index)
    elif any([x is not None for x in (index, count, reverse, rotation, callback)]):
        raise ValueError(
            "'index', 'count', 'reverse', 'rotation' or 'callback' set on stateless source: {!r}.".format(
            source))
    else:
        request = source

    return request
