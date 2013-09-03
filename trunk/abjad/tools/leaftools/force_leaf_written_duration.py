# -*- encoding: utf-8 -*-
from abjad.tools import durationtools


def force_leaf_written_duration(leaf, written_duration):
    r'''Forces `leaf` written duration to `written_duration`
    while preserving `leaf` duration.

    ..  container:: example

        **Example.** Renotate quarter note as dotted sixteenth note:

            >>> note = Note("c'4")
            >>> measure = Measure((1, 4), [note])
            >>> measure.append(note)
            >>> show(measure) # doctest: +SKIP

        ..  doctest::

            >>> f(measure)
            {
                \time 1/4
                c'4
            }

        ::

            >>> inspect(note).get_duration()
            Duration(1, 4)

        ::

        
            >>> leaftools.force_leaf_written_duration(note, Duration(3, 16))
            Note("c'8. * 4/3")
            >>> show(measure) # doctest: +SKIP

        ..  doctest::

            >>> f(measure)
            {
                \time 1/4
                c'8. * 4/3
            }

        ::

            >>> inspect(note).get_duration()
            Duration(1, 4)

        Note is now written as a dotted sixteenth (with an invisible
        LilyPond multiplier) even though note continues to
        have the duration of a quarter note.

    Adds LilyPond multiplier where necessary.

    Returns `leaf`.
    '''
    from abjad.tools import leaftools

    # check leaf type
    if not isinstance(leaf, leaftools.Leaf):
        raise TypeError('must be leaf: {!r}'.format(leaf))

    # check written duration type
    written_duration = durationtools.Duration(written_duration)

    # change leaf written duration
    previous = leaf._multiplied_duration
    leaf.written_duration = written_duration

    # change leaf multiplier if required
    leaf.lilypond_duration_multiplier = None
    multiplier = previous / leaf.written_duration
    if multiplier != 1:
        leaf.lilypond_duration_multiplier = multiplier

    # return leaf
    return leaf
