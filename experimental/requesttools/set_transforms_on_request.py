from experimental import helpertools


def set_transforms_on_request(request, index=None, count=None, reverse=None, rotation=None, callback=None):
    r'''.. versionadded:: 1.0

    Set transforms on `request`.

    Return `request`.
    '''
    from experimental import requesttools

    # check input
    assert isinstance(request, requesttools.Request)
    assert isinstance(index, (int, type(None))), repr(index)
    assert isinstance(count, (int, type(None))), repr(count)
    assert isinstance(reverse, (bool, type(None))), repr(count)
    assert isinstance(rotation, (int, type(None))), repr(count)
    assert isinstance(callback, (helpertools.Callback, type(None))), repr(callback)

    # set transforms
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

    # return request
    return request
