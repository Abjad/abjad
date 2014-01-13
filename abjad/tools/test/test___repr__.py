# -*- encoding: utf-8 -*-
import inspect
import pytest
from abjad.tools import datastructuretools
from abjad.tools import documentationtools
from abjad.tools import markuptools


# TODO: eventually make these work
_classes_to_skip = (
    )

classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___repr___01(class_):
    r'''All concrete classes have an interpreter representation.
    '''

    if not inspect.isabstract(class_):
        if class_ not in _classes_to_skip:
            instance = class_()
            string = repr(instance)
            assert string is not None
