from experimental.tools import helpertools


def set_transforms_on_request(request, index=None, count=None):
    r'''.. versionadded:: 1.0

    Set transforms on `request`.

    Return `request`.
    '''
    from experimental.tools import requesttools

    # check input
    assert isinstance(request, requesttools.Request)
    assert isinstance(index, (int, type(None))), repr(index)
    assert isinstance(count, (int, type(None))), repr(count)

    # set transforms
    if index is not None:
        request._index = index
    if count is not None:
        request._count = count

    # return request
    return request
