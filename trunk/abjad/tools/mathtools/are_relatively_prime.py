from abjad.tools.mathtools.factors import factors


def are_relatively_prime(expr):
    '''.. versionadded:: 2.5

    True when `expr` is a sequence comprising zero or more numbers,
    all of which are relatively prime::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.are_relatively_prime([13, 14, 15])
        True

    Otherwise false::

        abjad> mathtools.are_relatively_prime([13, 14, 15, 16])
        False

    Note that function returns true when `expr` is an empty sequence::

        abjad> mathtools.are_relatively_prime([])
        True

    Function returns false when `expr` is nonsensical type::

        abjad> mathtools.are_relatively_prime('foo')
        False

    Return boolean.
    '''

    try:
        all_factors = set([])
        for number in expr:
            cur_factors = factors(number)
            cur_factors.remove(1) 
            cur_factors = set(cur_factors)
            if all_factors & cur_factors:
                return False
            all_factors.update(cur_factors)
        return True
    except:
        return False
