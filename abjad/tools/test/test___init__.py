# -*- encoding: utf-8 -*-
import inspect
import pytest
import abjad
from abjad.tools import *
pytest.skip()


classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___init___01(class_):
    r'''All storage-formattable concrete classes initialize from empty input.
    '''

    if '_storage_format_specification' in dir(class_) and \
        not inspect.isabstract(class_):
        if hasattr(class_, '_default_positional_input_arguments'):
            args = class_._default_positional_input_arguments
            instance = class_(*args)
        else:
            instance = class_()
