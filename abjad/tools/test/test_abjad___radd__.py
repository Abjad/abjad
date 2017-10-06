import inspect
import pytest
from abjad.tools import documentationtools
from abjad.tools import datastructuretools
from abjad.tools import systemtools


ignored_classes = (
    datastructuretools.String,
    systemtools.StorageFormatManager,
    systemtools.FormatSpecification,
    )

classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('class_', classes)
def test_abjad___radd___01(class_):
    r'''Classes with __add__ also implement __radd__.
    '''
    if inspect.isabstract(class_):
        return
    if hasattr(class_, '__add__'):
        assert hasattr(class_, '__radd__')
