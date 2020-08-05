import inspect

import pytest

import abjad

ignored_classes = (
    abjad.Expression,
    abjad.FormatSpecification,
    abjad.MetricModulation,
    abjad.StorageFormatManager,
)

classes = abjad.list_all_classes(ignored_classes=ignored_classes)


@pytest.mark.parametrize("class_", classes)
def test_abjad___slots___01(class_):
    """
    All concrete classes defining __slots__ do not have a dict.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    attrs = inspect.classify_class_attrs(class_)
    attrs = dict((attr.name, attr) for attr in attrs)
    if "__slots__" not in attrs:
        return
    elif attrs["__slots__"].defining_class is not class_:
        return
    instance_one = class_()
    assert not hasattr(instance_one, "__dict__")
