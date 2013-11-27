# -*- encoding: utf-8 -*-
import inspect
import pickle
import pytest
from abjad.tools import documentationtools


classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test_pickle_01(class_):
    r'''All storage-formattable classes are pickable.
    '''

    if '_storage_format' in dir(class_) and not inspect.isabstract(class_):
        instance_one = class_()
        instance_two = pickle.loads(pickle.dumps(instance_one))
        assert instance_one == instance_two
