import abjad
import inspect
import pytest
from abjad.tools import documentationtools


ignored_classes = (
    abjad.FormatSpecification,
    abjad.Path,
    abjad.StorageFormatManager,
    abjad.Tags,
    )

classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('class_', classes)
def test_abjad___repr___01(class_):
    r'''All concrete classes have an interpreter representation.
    '''
    if inspect.isabstract(class_):
        return
    instance = class_()
    string = repr(instance)
    assert string is not None
    assert string != ''
