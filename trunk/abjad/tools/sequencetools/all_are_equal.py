def all_are_equal(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a sequence and all elements in `expr` are equal::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.all_are_equal([99, 99, 99, 99, 99, 99])
        True

    True when `expr` is an empty sequence::

        abjad> sequencetools.all_are_equal([])
        True

    False otherwise::

        abjad> sequencetools.all_are_equal(17)
        False

    Return boolean.
    '''

    try:
        first_element = None
        for element in expr:
            if first_element is None:
                first_element = element
            else:
                if not element == first_element:
                    return False
        return True
    except TypeError:
        return False
