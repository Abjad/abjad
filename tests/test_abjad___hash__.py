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
def test_abjad___hash___01(class_):
    """
    All concrete classes with __hash__ can hash.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    if getattr(class_, "__hash__", None) is None:
        return
    default_values = class_to_default_values.get(class_, ())
    instance = class_(*default_values)
    value = hash(instance)
    assert isinstance(value, int)
