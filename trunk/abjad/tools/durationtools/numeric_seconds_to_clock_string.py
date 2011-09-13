from fractions import Fraction


def numeric_seconds_to_clock_string(seconds):
    r'''.. versionadded:: 2.0

    Change numeric `seconds` to clock string::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.numeric_seconds_to_clock_string(117)
        '1\'57"'

    Return string.
    '''

    assert isinstance(seconds, (int, float, Fraction))
    if seconds < 0:
        raise ValueError('total seconds must be positive.')

    minutes = int(seconds / 60)
    remaining_seconds = str(int(seconds - minutes * 60)).zfill(2)
    clock_string = "%s'%s\"" % (minutes, remaining_seconds)

    return clock_string
