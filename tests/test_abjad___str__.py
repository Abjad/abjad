import inspect

import pytest
from _defaults import class_to_default_values

import abjad

_allowed_to_be_empty_string = (
    abjad.Accidental,
    abjad.CompoundOperator,
    abjad.Line,
    abjad.String,
    abjad.Tag,
)

ignored_classes = (
    abjad.FormatSpecification,
    abjad.MetricModulation,
)

classes = abjad.list_all_classes(ignored_classes=ignored_classes)


@pytest.mark.parametrize("class_", classes)
def test_abjad___str___01(class_):
    """
    All concrete classes have a string representation.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    if issubclass(class_, Exception):
        return
    default_values = class_to_default_values.get(class_, ())
    instance = class_(*default_values)
    string = str(instance)
    assert string is not None
    if class_ not in _allowed_to_be_empty_string:
        assert string != ""
