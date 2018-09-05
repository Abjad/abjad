import abjad
import inspect
import pytest


ignored_classes = (
    abjad.FormatSpecification,
    abjad.Path,
    abjad.StorageFormatManager,
    abjad.Tags,
    )

classes = pytest.helpers.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('class_', classes)
def test_abjad___hash___01(class_):
    """
    All concrete classes with __hash__ can hash.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, '_is_abstract', None) is True:
        return
    if getattr(class_, '__hash__', None) is None:
        return
    instance = class_()
    value = hash(instance)
    assert isinstance(value, int)
