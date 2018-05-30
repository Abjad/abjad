import numbers


def integer_equivalent_number_to_integer(number):
    """
    Changes integer-equivalent ``number`` to integer.

    ..  container:: example

        Returns integer-equivalent number as integer:

        >>> abjad.mathtools.integer_equivalent_number_to_integer(17.0)
        17

    ..  container:: example

        Returns noninteger-equivalent number unchanged:

        >>> abjad.mathtools.integer_equivalent_number_to_integer(17.5)
        17.5

    Returns number.
    """
    from abjad import mathtools
    if not isinstance(number, numbers.Number):
        message = 'must be number: {!r}.'
        message = message.format(number)
        raise TypeError(message)
    if mathtools.is_integer_equivalent_number(number):
        return int(number)
    else:
        return number
