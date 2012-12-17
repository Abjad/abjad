def index_to_slice_pair(index):
    r'''.. versionadded:: 1.0

    Change integer `index` to slice pair.
    '''

    assert isinstance(index, int), repr(index)

    if index == -1:
        return -1, None
    else:
        return index, index + 1
