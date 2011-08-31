from abjad import *


def test_contexttools_get_time_signature_mark_attached_to_component_01():

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    time_signature_mark = contexttools.get_time_signature_mark_attached_to_component(measure)

    assert time_signature_mark == contexttools.TimeSignatureMark((4, 8))
