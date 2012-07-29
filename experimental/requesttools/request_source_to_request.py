from experimental import helpertools
import copy


def request_source_to_request(source, callback=None, count=None, offset=None):
    r'''.. versionadded:: 1.0

    Change request `source` to request object.

    If `source` is one of ... ::

        StatalServer
        Handler

    ... then return ... ::

        StatalServerRequest
        HandlerRequest

    ... as output.

    If `source` is a ``SingleContextDivisionSelector`` then return updated
    ``SingleContextDivisionSelector``.

    If `source` is a constant then return `source` unchanged.

    If `source` is already a request then set `callback`, `count` or `offset`
    against `source` (if any are nonnone) and return `source`.
    '''
    from experimental import handlertools
    from experimental import requesttools
    from experimental import selectortools
    from experimental import statalservertools

    assert isinstance(callback, (helpertools.Callback, type(None))), repr(callback)
    assert isinstance(count, (int, type(None))), repr(count)
    assert isinstance(offset, (int, type(None))), repr(offset)

    if isinstance(source, requesttools.Request):
        request = source
        if callback is not None:
            request.callback = callback
        if count is not None:
            request.count = count
        if offset is not None:
            request.offset = offset
    elif isinstance(source, statalservertools.StatalServer):
        if count is not None or offset is not None:
            request = requesttools.StatalServerRequest(source, count=count, offset=offset)
    elif isinstance(source, handlertools.Handler):
        if offset is not None:
            assert count is None
            request = requesttools.HandlerRequest(source, offset=offset)
    elif isinstance(source, selectortools.SingleContextDivisionSliceSelector):
        if any([x is not None for x in (callback, count, offset)]):
            request = copy.copy(source)
            request.callback = callback
            request.count = count
            request.offset = offset
    elif any([x is not None for x in (callback, count, offset)]):
        raise ValueError("'callback', 'count' or 'offset' set on nonstatal source: {!r}.".format(source))
    else:
        request = source

    return request
