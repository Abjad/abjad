# probably better with regular expression handling
def interval_string_to_pair_and_indicators(interval_string):
    r'''.. versionadded:: 1.0

    Change `interval_string` to pair, boolean start indicator and
    boolean stop indicator::

        >>> mathtools.interval_string_to_pair_and_indicators('[5, 8)')
        ((5, 8), False, True)

    Parse square brackets as closed interval bounds.

    Parse parentheses as open interval bounds.

    Return triple.
    '''

    assert isinstance(interval_string, str)
    spaceless_interval_string = interval_string.replace(' ', '')
    left, right = spaceless_interval_string.split(',')
    if left[0] == '(':
        is_left_open = True
    elif left[0] == '[':
        is_left_open = False
    else:
        raise ValueError(
            'can not initialize interval start from {!r}.'.format(interval_string))

    # probably attackable
    start = eval(left[1:])
    if right[-1] == ')':
        is_right_open = True
    elif right[-1] == ']':
        is_right_open = False
    else:
        raise ValueError(
            'can not initialize interval stop from {!r}.'.format(interval_string))

    # probably attackable
    stop = eval(right[:-1])
    pair = start, stop
    return pair, is_left_open, is_right_open
