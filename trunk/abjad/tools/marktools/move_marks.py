from abjad.tools import componenttools


def move_marks(donor, recipient):
    r'''.. versionadded 2.9

    Move marks from `donor` component to `recipient` component::

        >>> staff = Staff(r'\clef "bass" c \staccato d e f')

    ::

        >>> f(staff)
        \new Staff {
            \clef "bass"
            c4 -\staccato
            d4
            e4
            f4
        }

    ::

        >>> marktools.move_marks(staff[0], staff[2])
        [Articulation('staccato')(e4), ClefMark('bass')(e4)]

    ::

        >>> f(staff)
        \new Staff {
            c4
            d4
            \clef "bass"
            e4 -\staccato
            f4
        }

    Return list of marks moved.
    '''
    from abjad.tools import marktools

    assert isinstance(donor, componenttools.Component)
    assert isinstance(recipient, componenttools.Component)

    result = []
    for mark in marktools.get_marks_attached_to_component(donor):
        result.append(mark.attach(recipient))

    return result
