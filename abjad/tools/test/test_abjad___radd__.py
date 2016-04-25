# -*- coding: utf-8 -*-
import inspect
import pytest
from abjad.tools import documentationtools


ignored_classes = (
    )

classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.skip('Correct failing classes.')
@pytest.mark.parametrize('class_', classes)
def test_abjad___radd___01(class_):
    r'''All classes implementing __add__ also implement __radd__.
    '''
    if inspect.isabstract(class_):
        return
    if hasattr(class_, '__add__'):
        assert hasattr(class_, '__radd__')
