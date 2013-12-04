# -*- encoding: utf-8 -*-
import pytest
from abjad.tools import documentationtools
pytest.skip()


classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___repr___01(class_):
    r'''All classes have an interpreter representation.
    '''

    assert '__repr__' in dir(class_)
    if '_repr_specification' in dir(class_) and not inspect.isabstract(class_):
        instance = class_()
        string = repr(instance_)
