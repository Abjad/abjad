def detach_marks_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Detach marks attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.SlurSpanner(staff.select_leaves())
        >>> marktools.Articulation('^')(staff[0])
        Articulation('^')(c'8)
        >>> marktools.LilyPondComment('comment 1')(staff[0])
        LilyPondComment('comment 1')(c'8)
        >>> marktools.LilyPondCommandMark('slurUp')(staff[0])
        LilyPondCommandMark('slurUp')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            % comment 1
            \slurUp
            c'8 -\marcato (
            d'8
            e'8
            f'8 )
        }

    ::

        >>> for mark in staff[0].get_marks():
        ...     mark
        ...
        Articulation('^')(c'8)
        LilyPondComment('comment 1')(c'8)
        LilyPondCommandMark('slurUp')(c'8)

    ::

        >>> for mark in marktools.detach_marks_attached_to_component(staff[0]):
        ...     mark
        ...
        Articulation('^')
        LilyPondComment('comment 1')
        LilyPondCommandMark('slurUp')

    ::

        >>> staff[0].get_marks()
        ()

    Return tuple or zero or more marks detached.
    '''
    from abjad.tools import marktools

    marks = []
    for mark in component.get_marks():
        mark.detach()
        marks.append(mark)

    return tuple(marks)
