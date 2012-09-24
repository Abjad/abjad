from abjad.tools import notetools


def iterate_notes_in_expr(expr, reverse=False, start=0, stop=None):
    r'''.. versionadded:: 2.10

    Yield left-to-right notes in `expr`::

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

        >>> for note in iterationtools.iterate_notes_in_expr(staff):
        ...     note
        ...
        Note("c'8")
        Note("d'8")
        Note("e'8")
        Note("f'8")
        Note("g'8")
        Note("a'8")

    Use optional `start` and `stop` keyword parameters to control
    start and stop indices of iteration::

        >>> for note in iterationtools.iterate_notes_in_expr(staff, start=3):
        ...     note
        ...
        Note("f'8")
        Note("g'8")
        Note("a'8")

    ::

        >>> for note in iterationtools.iterate_notes_in_expr(staff, start=0, stop=3):
        ...     note
        ...
        Note("c'8")
        Note("d'8")
        Note("e'8")

    ::

        >>> for note in iterationtools.iterate_notes_in_expr(staff, start=2, stop=4):
        ...     note
        ...
        Note("e'8")
        Note("f'8")

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

        >>> for note in iterationtools.iterate_notes_in_expr(staff, reverse=True):
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

        >>> for note in iterationtools.iterate_notes_in_expr(staff, reverse=True, start=3):
        ...     note
        ...
        Note("e'8")
        Note("d'8")
        Note("c'8")

    ::

        >>> for note in iterationtools.iterate_notes_in_expr(staff, reverse=True, start=0, stop=3):
        ...     note
        ...
        Note("a'8")
        Note("g'8")
        Note("f'8")

    ::

        >>> for note in iterationtools.iterate_notes_in_expr(staff, reverse=True, start=2, stop=4):
        ...     note
        ...
        Note("f'8")
        Note("e'8")


    Ignore threads.

    Return generator.
    '''
    from abjad.tools import iterationtools

    return iterationtools.iterate_components_in_expr(
        expr, klass=notetools.Note, reverse=reverse, start=start, stop=stop)
