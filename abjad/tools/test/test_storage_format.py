# -*- encoding: utf-8 -*-
import inspect
import pytest
import abjad
from abjad import demos
from abjad.tools import documentationtools
pytest.skip()


classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test_storage_format_01(class_):
    r'''All storage-formattable classes have evaluable storage format.
    '''

    if '_storage_format_specification' in dir(class_) and \
        not inspect.isabstract(class_):
        environment = abjad.__dict__.copy()
        environment.update(demos.__dict__)
        if hasattr(class_, '_default_positional_input_arguments'):
            args = class_._default_positional_input_arguments
            instance_one = class_(*args)
        else:
            instance_one = class_()
        instance_one_format = format(instance_one, 'storage')
        instance_two = eval(instance_one_format, environment)
        instance_two_format = format(instance_two, 'storage')
        assert instance_one_format == instance_two_format
