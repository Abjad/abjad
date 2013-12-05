# -*- encoding: utf-8 -*-
import inspect
import pickle
import pytest
import abjad
from abjad.tools import documentationtools
pytest.skip()


classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test_pickle_01(class_):
    r'''All storage-formattable classes are pickable.
    '''

    if '_storage_format_specification' in dir(class_) and \
        not inspect.isabstract(class_):
        if hasattr(class_, '_default_positional_input_arguments'):
            args = class_._default_positional_input_arguments
            instance_one = class_(*args)
        else:
            instance_one = class_()
        pickle_string = pickle.dumps(instance_one)
        instance_two = pickle.loads(pickle_string)
        instance_one_format = format(instance_one, 'storage')
        instance_two_format = format(instance_two, 'storage')
        assert instance_one_format == instance_two_format
