from abjad.exceptions import ExtraMarkError
from abjad.exceptions import MissingMarkError
from abjad.tools.marktools.get_annotations_attached_to_component import get_annotations_attached_to_component


def get_annotation_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get exactly one annotation attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> marktools.Annotation('special information')(staff[0])
        Annotation('special information')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> marktools.get_annotation_attached_to_component(staff[0])
        Annotation('special information')(c'8)

    Return one annotation.

    Raise missing mark error when no annotation is attached.

    Raise extra mark error when more than one annotation is attached.
    '''

    annotations = get_annotations_attached_to_component(component)
    if not annotations:
        raise MissingMarkError
    elif 1 < len(annotations):
        raise ExtraMarkError
    else:
        return annotations[0]
