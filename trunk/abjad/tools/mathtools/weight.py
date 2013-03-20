def weight(sequence):
    '''Sum of the absolute value of the elements in `sequence`:

    ::

        >>> mathtools.weight([-1, -2, 3, 4, 5])
        15

    Return nonnegative integer.
    '''

    return sum([abs(element) for element in sequence])
