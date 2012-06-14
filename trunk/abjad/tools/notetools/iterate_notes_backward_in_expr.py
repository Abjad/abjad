from abjad.tools import componenttools


def iterate_notes_backward_in_expr(expr, start=0, stop=None):
    r'''.. versionadded:: 2.0

    Yield right-to-left notes in `expr`::

        >>> staff = Staff()
        >>> staff.append(Measure((2, 8), "c'8 d'8"))
        >>> staff.append(Measure((2, 8), "e'8 f'8"))
        >>> staff.append(Measure((2, 8), "g'8 a'8"))

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
        }

    ::

        >>> for note in notetools.iterate_notes_backward_in_expr(staff):
        ...     note
        ...
        Note("a'8")
        Note("g'8")
        Note("f'8")
        Note("e'8")
        Note("d'8")
        Note("c'8")

    Use optional `start` and `stop` keyword parameters to control
    indices of iteration::

        >>> for note in notetools.iterate_notes_backward_in_expr(staff, start=3):
        ...     note
        ...
        Note("e'8")
        Note("d'8")
        Note("c'8")

    ::

        >>> for note in notetools.iterate_notes_backward_in_expr(staff, start=0, stop=3):
        ...     note
        ...
        Note("a'8")
        Note("g'8")
        Note("f'8")

    ::

        >>> for note in notetools.iterate_notes_backward_in_expr(staff, start=2, stop=4):
        ...     note
        ...
        Note("f'8")
        Note("e'8")

    Return note generator.

    .. versionchanged:: 2.0
        renamed ``iterate.notes_backward_in()`` to
        ``notetools.iterate_notes_backward_in_expr()``.
    '''
    from abjad.tools import notetools

    return componenttools.iterate_components_backward_in_expr(expr, notetools.Note, start=start, stop=stop)
