# -*- encoding: utf-8 -*-
import copy
import inspect
import pytest
from abjad.tools import documentationtools


classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___copy___01(class_):
    r'''All objects with a storage format can copy.
    '''

    if '_storage_format_specification' in dir(class_) and \
        not inspect.isabstract(class_):
        instance_one = class_()
        instance_two = copy.copy(instance_one)
        instance_one_format = format(instance_one, 'storage')
        instance_two_format = format(instance_two, 'storage')
        assert instance_one_format == instance_two_format
        #assert instance_one == instance_two
