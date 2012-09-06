import copy


def concatenate_pitch_arrays(pitch_arrays):
    '''.. versionadded:: 2.0

    Concatenate `pitch_arrays`::

        >>> array_1 = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])
        >>> print array_1
        [ ] [     ] [ ]
        [     ] [ ] [ ]

    ::

        >>> array_2 = pitcharraytools.PitchArray([[3, 4], [4, 3]])
        >>> print array_2
        [     ] [           ]
        [           ] [     ]

    ::

        >>> array_3 = pitcharraytools.PitchArray([[1, 1], [1, 1]])
        >>> print array_3
        [ ] [ ]
        [ ] [ ]

    ::

        >>> merged_array = pitcharraytools.concatenate_pitch_arrays([array_1, array_2, array_3])
        >>> print merged_array
        [ ] [     ] [ ] [     ] [           ] [ ] [ ]
        [     ] [ ] [ ] [           ] [     ] [ ] [ ]

    Return pitch array.
    '''
    from abjad.tools import pitcharraytools

    if not all([isinstance(x, pitcharraytools.PitchArray) for x in pitch_arrays]):
        raise TypeError('must be pitch arrays.')

    if not pitch_arrays:
        return pitcharraytools.PitchArray()

    merged_array = copy.copy(pitch_arrays[0])
    for pitch_array in pitch_arrays[1:]:
        merged_array += pitch_array

    return merged_array
