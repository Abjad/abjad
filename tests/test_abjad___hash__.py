import inspect

import pytest

import abjad

ignored_classes = (
    abjad.FormatSpecification,
    abjad.MetricModulation,
    abjad.StorageFormatManager,
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
    instance = class_()
    value = hash(instance)
    assert isinstance(value, int)
