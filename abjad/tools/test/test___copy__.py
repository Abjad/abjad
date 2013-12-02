# -*- encoding: utf-8 -*-
import copy
import inspect
import pytest
from abjad import *


classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___copy___01(class_):
    r'''All objects with a storage format can copy.
    '''

    if '_storage_format_specification' in dir(class_) and \
        not inspect.isabstract(class_):
        instance_one = class_()
        instance_two = copy.copy(instance_one)
        assert instance_one == instance_two
