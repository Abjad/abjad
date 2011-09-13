from abjad.tools.marktools.Annotation import Annotation


def get_annotations_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get annotations attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> marktools.Annotation('annotation 1')(staff[0])
        Annotation('annotation 1')(c'8)
        abjad> marktools.Annotation('annotation 2')(staff[0])
        Annotation('annotation 2')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> marktools.get_annotations_attached_to_component(staff[0])
        (Annotation('annotation 1')(c'8), Annotation('annotation 2')(c'8))

    Return tuple of zero or more annotations.
    '''

    result = []
    for mark in component._marks_for_which_component_functions_as_start_component:
        if isinstance(mark, Annotation):
            result.append(mark)

    result = tuple(result)
    return result
