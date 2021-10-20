import inspect

import pytest
from _defaults import class_to_default_values

import abjad

ignored_classes = (
    abjad.FormatSpecification,
    abjad.MetricModulation,
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
    default_values = class_to_default_values.get(class_, ())
    instance_one = class_(*default_values)
    assert not hasattr(instance_one, "__dict__")
