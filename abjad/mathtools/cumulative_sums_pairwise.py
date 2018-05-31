# TODO: move to Sequence
def cumulative_sums_pairwise(argument):
    """
    Gets pairwise cumulative sums of ``argument`` from zero.

    ..  container:: example

        >>> abjad.mathtools.cumulative_sums_pairwise([1, 2, 3, 4, 5, 6])
        [(0, 1), (1, 3), (3, 6), (6, 10), (10, 15), (15, 21)]

    Returns pairs in new object of ``argument`` type.
    """
    import abjad
    sums = abjad.mathtools.cumulative_sums(argument)
    pairs = abjad.sequence(sums).nwise()
    return type(argument)([tuple(_) for _ in pairs])
