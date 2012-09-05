def detach_annotations_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Detach annotations attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.SlurSpanner(staff.leaves)
        >>> marktools.Annotation('annotation 1')(staff[0])
        Annotation('annotation 1')(c'8)
        >>> marktools.Annotation('annotation 2')(staff[0])
        Annotation('annotation 2')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }


    ::

        >>> marktools.get_annotations_attached_to_component(staff[0])
        (Annotation('annotation 1')(c'8), Annotation('annotation 2')(c'8))

    ::

        >>> marktools.detach_annotations_attached_to_component(staff[0])
        (Annotation('annotation 1'), Annotation('annotation 2'))

    ::

        >>> marktools.get_annotations_attached_to_component(staff[0])
        ()

    Return tuple or zero or more annotations detached.
    '''
    from abjad.tools import marktools

    annotations = []
    for annotation in marktools.get_annotations_attached_to_component(component):
        annotation.detach()
        annotations.append(annotation)

    return tuple(annotations)
