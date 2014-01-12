# -*- encoding: utf-8 -*-
import inspect
import pytest
from abjad.tools import documentationtools
pytest.skip()


classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___repr___01(class_):
    r'''All concrete classes have an interpreter representation.
    '''

    if not inspect.isabstract(class_):
        instance = class_()
        string = repr(instance)
        assert string is not None
