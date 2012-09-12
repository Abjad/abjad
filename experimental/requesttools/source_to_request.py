import copy
from experimental import helpertools


def source_to_request(source, index=None, count=None, reverse=None, rotation=None, callback=None):
    r'''.. versionadded:: 1.0

    Change request `source` to request object.

    If `source` is one of ... ::

        StatalServer
        Handler

    ... then return ... ::

        StatalServerRequest
        HandlerRequest

    ... as output.

    Set any of `index`, `count`, `reverse`, `rotation` or 
    `callback` that are not none against request
    and return request.

    If `source` is a list or tuple then apply any 
    of `index`, `count`, `reverse`, `rotation` or 
    `callback` that are not none against `source`
    and return `source`.

    If `source` tests as none of the above then
    return `source` unchanged.
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
        return request
    elif isinstance(source, statalservertools.StatalServer):
        request = requesttool.StatalServerRequest(source)
        return source_to_request(
            request, index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)
    elif isinstance(source, handlertools.Handler):
        request = requesttool.HandlerRequest(source)
        return source_to_request(
            request, index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)
    elif isinstance(source, (list, tuple)):
        request = requesttools.Request(
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)
        source = requesttools.apply_request_transforms(request, source)
        return source
    else:
        return source
