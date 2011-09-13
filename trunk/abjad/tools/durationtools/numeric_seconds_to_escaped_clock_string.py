from fractions import Fraction


def numeric_seconds_to_escaped_clock_string(seconds):
    r'''.. versionadded:: 2.0

    Change numeric `seconds` to escaped clock string::

        abjad> from abjad.tools import durationtools

    ::

        abjad> note = Note("c'4")
        abjad> clock_string = durationtools.numeric_seconds_to_escaped_clock_string(117)
        abjad> markuptools.Markup('"%s"' % clock_string, 'up')(note)
        Markup('"1\'57\\""', 'up')

    ::

        abjad> f(note)
        c'4 ^ \markup { "1'57\"" }

    Escape seconds indicator for output as LilyPond markup.

    Return string.
    '''

    assert isinstance(seconds, (int, float, Fraction))
    if seconds < 0:
        raise ValueError('total seconds must be positive.')

    minutes = int(seconds / 60)
    remaining_seconds = str(int(seconds - minutes * 60)).zfill(2)
    clock_string = "%s'%s\\\"" % (minutes, remaining_seconds)

    return clock_string
