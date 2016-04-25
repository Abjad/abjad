from abjad import *


def test_agenttools_InspectionAgent_get_annotation_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    annotation = indicatortools.Annotation('special dictionary', {})
    attach(annotation, staff[0])

    assert inspect_(staff[0]).get_annotation('special dictionary') == {}
