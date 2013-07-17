def get_annotations_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get annotations attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> marktools.Annotation('annotation 1')(staff[0])
        Annotation('annotation 1')(c'8)
        >>> marktools.Annotation('annotation 2')(staff[0])
        Annotation('annotation 2')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> marktools.get_annotations_attached_to_component(staff[0])
        (Annotation('annotation 1')(c'8), Annotation('annotation 2')(c'8))

    Return tuple of zero or more annotations.
    '''
    from abjad.tools import marktools

#    result = []
#    for mark in component._start_marks:
#        if isinstance(mark, marktools.Annotation):
#            result.append(mark)
#
#    result = tuple(result)
#    return result

    return component.get_marks(marktools.Annotation)
