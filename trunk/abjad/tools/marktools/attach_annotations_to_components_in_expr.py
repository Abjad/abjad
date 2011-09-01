from abjad.tools.marktools.Annotation import Annotation


def attach_annotations_to_components_in_expr(expr, annotations):
    r'''.. versionadded:: 2.3

    Attach `annotations` to components in `expr`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> annotation = marktools.Annotation('foo', 'bar')
        abjad> marktools.attach_annotations_to_components_in_expr(staff.leaves, [annotation])

    ::

        abjad> for x in staff:
        ...     print x, marktools.get_annotations_attached_to_component(x)
        ... 
        c'8 (Annotation('foo', 'bar')(c'8),)
        d'8 (Annotation('foo', 'bar')(d'8),)
        e'8 (Annotation('foo', 'bar')(e'8),)
        f'8 (Annotation('foo', 'bar')(f'8),)

    Return none.
    '''
    from abjad.tools import componenttools

    for component in componenttools.iterate_components_forward_in_expr(expr):
        for annotation in annotations:
            Annotation(annotation)(component)
