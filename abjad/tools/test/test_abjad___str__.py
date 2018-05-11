import abjad
import inspect
import pytest
from abjad.tools import documentationtools
from abjad.tools import tonalanalysistools


_allowed_to_be_empty_string = (
    abjad.Accidental,
    abjad.Articulation,
    abjad.CompoundOperator,
    abjad.Line,
    abjad.Postscript,
    abjad.SchemeColor,
    abjad.String,
    abjad.Tag,
    tonalanalysistools.ChordSuspension,
    )

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
def test_abjad___str___01(class_):
    r'''All concrete classes have a string representation.

    With the exception of the exception classes. And those classes listed
    explicitly here.
    '''
    if inspect.isabstract(class_):
        return
    if issubclass(class_, Exception):
        return
    instance = class_()
    string = str(instance)
    assert string is not None
    if class_ not in _allowed_to_be_empty_string:
        assert string != ''
