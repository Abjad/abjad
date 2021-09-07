import inspect

import pytest

import abjad

ignored_classes = (abjad.FormatSpecification,)

classes = abjad.list_all_classes(ignored_classes=ignored_classes)


@pytest.mark.parametrize("class_", classes)
def test_abjad___rmul___01(class_):
    """
    All classes implementing __mul__ also implement __rmul__.
    """
    if inspect.isabstract(class_):
        return
    if hasattr(class_, "__mul__"):
        assert hasattr(class_, "__rmul__")
