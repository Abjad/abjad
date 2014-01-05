# -*- encoding: utf-8 -*-
import inspect
import pytest
from abjad.tools import documentationtools
#pytest.skip()


classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___repr___01(class_):
    r'''All classes have an interpreter representation.
    '''

    if inspect.isabstract(class_):
        continue
    if hasattr(class_, '_default_positional_input_arguments'):
        args = class_._default_positional_input_arguments
        instance = class_(*args)
    else:
        instance = class_()
    string = repr(instance)
    assert string is not None
