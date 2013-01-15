def durations_to_integers(durations):
    '''Change `durations` to integers:

    ::

        >>> durations = [Duration(2, 4), 3, '8.', (5, 16)]
        >>> for integer in durationtools.durations_to_integers(durations):
        ...     integer
        ...
        8
        48
        3
        5

    Return new object of `durations` type.
    '''
    from abjad.tools import durationtools

    # change to nonreduced fracxtions
    nonreduced_fractions = durationtools.durations_to_nonreduced_fractions_with_common_denominator(
        durations)

    # find common denominator
    common_denominator = nonreduced_fractions[0].denominator

    # change to integers
    nonreduced_fractions = [
        common_denominator * nonreduced_fraction for nonreduced_fraction in nonreduced_fractions]
    fractions = [nonreduced_fraction.reduce() for nonreduced_fraction in nonreduced_fractions]
    assert all([fraction.denominator == 1 for fraction in fractions])
    integers = [fraction.numerator for fraction in fractions]
    
    # return integers
    return integers
