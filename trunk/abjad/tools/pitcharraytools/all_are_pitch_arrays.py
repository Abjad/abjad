from abjad.tools.pitcharraytools.PitchArray import PitchArray


def all_are_pitch_arrays(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad pitch arrays::

        >>> from abjad.tools import pitcharraytools

    ::

        >>> pitch_array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

    ::

        >>> pitcharraytools.all_are_pitch_arrays([pitch_array])
        True

    True when `expr` is an empty sequence::

        >>> pitcharraytools.all_are_pitch_arrays([])
        True

    Otherwise false::

        >>> pitcharraytools.all_are_pitch_arrays('foo')
        False

    Return boolean.
    '''

    return all([isinstance(x, PitchArray) for x in expr])
