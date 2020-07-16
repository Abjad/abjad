import inspect

import pytest

import abjad

ignored_classes = (
    abjad.FormatSpecification,
    abjad.MetricModulation,
    abjad.Path,
    abjad.StorageFormatManager,
)

classes = pytest.helpers.list_all_abjad_classes(ignored_classes=ignored_classes)


@pytest.mark.parametrize("class_", classes)
def test_abjad___repr___01(class_):
    """
    All concrete classes have an interpreter representation.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    instance = class_()
    string = repr(instance)
    assert string is not None
    assert string != ""
