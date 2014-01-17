# -*- encoding: utf-8 -*-
import inspect
import pytest
import abjad
from abjad.tools import datastructuretools
from abjad.tools import documentationtools
from abjad.tools import tonalanalysistools


classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___format___01(class_):
    r'''All concrete classes have a storage format.
    '''

    if '_storage_format_specification' in dir(class_) and \
        not inspect.isabstract(class_):
        instance = class_()
        instance_format = format(instance, 'storage')
        assert isinstance(instance_format, str)
        assert not instance_format == ''


# TODO: make these work eventually
_classes_to_temporarily_skip = (
    datastructuretools.ContextMap,
    tonalanalysistools.RootedChordClass,
    )

classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___format___02(class_):
    r'''All storage-formattable classes have evaluable storage format.
    '''
    pytest.skip()

    if '_storage_format_specification' in dir(class_) and \
        not inspect.isabstract(class_) and \
        class_ not in _classes_to_temporarily_skip:
        environment = abjad.__dict__.copy()
        environment.update(abjad.demos.__dict__)
        instance_one = class_()
        instance_one_format = format(instance_one, 'storage')
        assert isinstance(instance_one_format, str)
        assert instance_one_format != ''
        instance_two = eval(instance_one_format, environment)
#        instance_two_format = format(instance_two, 'storage')
#        assert instance_one_format == instance_two_format
