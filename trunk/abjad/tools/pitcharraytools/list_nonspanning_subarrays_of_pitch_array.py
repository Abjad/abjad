from abjad.tools import sequencetools


def list_nonspanning_subarrays_of_pitch_array(pitch_array):
    r'''.. versionadded:: 2.0

    List nonspanning subarrays of `pitch_array`::

        >>> array = pitcharraytools.PitchArray([
        ...     [2, 2, 3, 1],
        ...     [1, 2, 1, 1, 2, 1],
        ...     [1, 1, 1, 1, 1, 1, 1, 1]])
        >>> print array
        [     ] [     ] [           ] [ ]
        [ ] [     ] [ ] [ ] [     ] [ ]
        [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]

    ::

        >>> subarrays = pitcharraytools.list_nonspanning_subarrays_of_pitch_array(array)
        >>> len(subarrays)
        3

    ::

        >>> print subarrays[0]
        [     ] [     ]
        [ ] [     ] [ ]
        [ ] [ ] [ ] [ ]

    ::

        >>> print subarrays[1]
        [           ]
        [ ] [     ]
        [ ] [ ] [ ]

    ::

        >>> print subarrays[2]
        [ ]
        [ ]
        [ ]

    Return list.
    '''
    from abjad.tools import pitcharraytools

    if not isinstance(pitch_array, pitcharraytools.PitchArray):
        raise TypeError('must be pitch array.')

    unspanned_indices = []
    for i in range(pitch_array.width + 1):
        if not pitch_array.has_spanning_cell_over_index(i):
            unspanned_indices.append(i)

    array_depth = pitch_array.depth
    subarrays = []
    for start_column, stop_column in sequencetools.iterate_sequence_pairwise_strict(unspanned_indices):
        upper_left_pair = (0, start_column)
        lower_right_pair = (array_depth, stop_column)
        subarray = pitch_array.copy_subarray(upper_left_pair, lower_right_pair)
        subarrays.append(subarray)

    return subarrays
