def all_are_equal(argument):
    """
    Is true when ``argument`` is an iterable collection of equal items.

    ..  container:: example

        >>> abjad.mathtools.all_are_equal([99, 99, 99, 99, 99, 99])
        True

        >>> abjad.mathtools.all_are_equal(17)
        False

    ..  container:: example

        Is true when ``argument`` is empty:

        >>> abjad.mathtools.all_are_equal([])
        True

    Returns true or false.
    """
    try:
        first_element = None
        for element in argument:
            if first_element is None:
                first_element = element
            else:
                if not element == first_element:
                    return False
        return True
    except TypeError:
        return False
