# -*- encoding: utf-8 -*-
import inspect
import pytest
import abjad
from abjad.tools import datastructuretools
from abjad.tools import documentationtools
from abjad.tools import markuptools


# TODO: make these classes empty-initializable
_classes_to_ignore = (
    markuptools.Markup,
    )

classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___init___01(class_):
    r'''All concrete classes initialize from empty input.
    '''

    if not inspect.isabstract(class_):
        if class_ not in _classes_to_ignore:
            instance = class_()
