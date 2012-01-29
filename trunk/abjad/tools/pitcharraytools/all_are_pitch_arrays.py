from abjad.tools.pitcharraytools.PitchArray import PitchArray


def all_are_pitch_arrays(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad pitch arrays::

        abjad> from abjad.tools import pitcharraytools

    ::

        abjad> pitch_array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

    ::

        abjad> pitcharraytools.all_are_pitch_arrays([pitch_array])
        True

    True when `expr` is an empty sequence::

        abjad> pitcharraytools.all_are_pitch_arrays([])
        True

    Otherwise false::

        abjad> pitcharraytools.all_are_pitch_arrays('foo')
        False

    Return boolean.
    '''

    return all([isinstance(x, PitchArray) for x in expr])
