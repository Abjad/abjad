from abjad import *


def test_marktools_get_value_of_annotation_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    dictionary = {'foo': 'bar'}
    marktools.Annotation('special dictionary', dictionary)(staff[0])
    marktools.Annotation('foo', 'bar')(staff[0])

    value = marktools.get_value_of_annotation_attached_to_component(staff[0], 'special dictionary')
    assert value == dictionary

    value = marktools.get_value_of_annotation_attached_to_component(staff[0], 'foo')
    assert value == 'bar'

    value = marktools.get_value_of_annotation_attached_to_component(staff[0], 'blah', 'default')
    assert value == 'default'
