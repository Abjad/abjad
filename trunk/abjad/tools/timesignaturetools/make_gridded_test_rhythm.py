from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools


def make_gridded_test_rhythm(grid_length, rhythm_number, denominator=16):
    r'''.. versionadded:: 2.11

    Make test rhythm number `rhythm_number` that fits `grid_length`.

    Return selection of one or more possibly tied notes.

    Example 1. The eight test rhythms that fit a length-``4`` grid::

        >>> for rhythm_number in range(8):
        ...     notes = timesignaturetools.make_gridded_test_rhythm(
        ...         4, rhythm_number, denominator=4)
        ...     measure = Measure((4, 4), notes)
        ...     print '{}\t{}'.format(rhythm_number, measure)
        ...
        0   |4/4, c'1|
        1   |4/4, c'2., c'4|
        2   |4/4, c'2, c'4, c'4|
        3   |4/4, c'2, c'2|
        4   |4/4, c'4, c'4, c'2|
        5   |4/4, c'4, c'4, c'4, c'4|
        6   |4/4, c'4, c'2, c'4|
        7   |4/4, c'4, c'2.|

    Example 2. The sixteenth test rhythms for that a length-``5`` grid::

        >>> for rhythm_number in range(16):
        ...     notes = timesignaturetools.make_gridded_test_rhythm(
        ...         5, rhythm_number, denominator=4)
        ...     measure = Measure((5, 4), notes)
        ...     print '{}\t{}'.format(rhythm_number, measure)
        ...
        0   |5/4, c'1, c'4|
        1   |5/4, c'1, c'4|
        2   |5/4, c'2., c'4, c'4|
        3   |5/4, c'2., c'2|
        4   |5/4, c'2, c'4, c'2|
        5   |5/4, c'2, c'4, c'4, c'4|
        6   |5/4, c'2, c'2, c'4|
        7   |5/4, c'2, c'2.|
        8   |5/4, c'4, c'4, c'2.|
        9   |5/4, c'4, c'4, c'2, c'4|
        10  |5/4, c'4, c'4, c'4, c'4, c'4|
        11  |5/4, c'4, c'4, c'4, c'2|
        12  |5/4, c'4, c'2, c'2|
        13  |5/4, c'4, c'2, c'4, c'4|
        14  |5/4, c'4, c'2., c'4|
        15  |5/4, c'4, c'1|

    Use for testing metrical hierarchy establishment.
    '''
    from abjad.tools import notetools

    # check input
    assert mathtools.is_positive_integer(grid_length)
    assert isinstance(rhythm_number, int)
    assert mathtools.is_positive_integer_power_of_two(denominator)

    # find count of all rhythms that fit grid length
    rhythm_count = 2 ** (grid_length - 1)

    # read rhythm number cyclically to allow large and negative rhythm numbers
    rhythm_number = rhythm_number % rhythm_count

    # find binary representation of rhythm
    binary_representation = mathtools.integer_to_binary_string(rhythm_number)
    binary_representation = binary_representation.zfill(grid_length)

    # partition binary representation of rhythm
    parts = sequencetools.partition_sequence_by_value_of_elements(binary_representation)

    # find durations
    durations = [durationtools.Duration(len(part), denominator) for part in parts]

    # make notes
    notes = notetools.make_notes([0], durations)

    # return notes
    return notes
