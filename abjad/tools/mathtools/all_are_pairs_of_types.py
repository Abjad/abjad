def all_are_pairs_of_types(argument, first_type, second_type):
    """
    Is true when ``argument`` is an iterable collection whose members are all
    of length 2, and where the first member of each pair is an instance of
    ``first_type`` and where the second member of each pair is an instance of
    ``second_type``.

    ..  container:: example

        >>> items = [(1., 'a'), (2.1, 'b'), (3.45, 'c')]
        >>> abjad.mathtools.all_are_pairs_of_types(items, float, str)
        True

        >>> abjad.mathtools.all_are_pairs_of_types('foo', float, str)
        False

    ..  container:: example

        Is true when ``argument`` is empty:

        >>> abjad.mathtools.all_are_pairs_of_types([], float, str)
        True

    Returns true or false.
    """
    try:
        return all(
            (len(_) == 2 and
            isinstance(_[0], first_type) and
            isinstance(_[1], second_type))
            for _ in argument
            )
    except (KeyError, TypeError):
        return False
