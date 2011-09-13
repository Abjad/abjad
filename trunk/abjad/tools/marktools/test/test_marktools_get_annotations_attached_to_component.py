from abjad import *


def test_marktools_get_annotations_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    annotation_1 = marktools.Annotation('annotation 1')(staff[0])
    annotation_2 = marktools.Annotation('annotation 2')(staff[0])

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    annotations = marktools.get_annotations_attached_to_component(staff[0])
    assert annotations == (annotation_1, annotation_2)
