import abjad
import inspect
import pytest
import abjad.book
from abjad.tools import documentationtools


ignored_classes = (
    abjad.Enumeration,
    abjad.FormatSpecification,
    abjad.Path,
    abjad.StorageFormatManager,
    abjad.Tags,
    abjad.TestCase,
    abjad.book.AbjadDirective,
    abjad.book.CodeBlock,
    abjad.book.CodeOutputProxy,
    abjad.book.AbjadDoctestDirective,
    abjad.book.GraphvizOutputProxy,
    abjad.book.ImportDirective,
    abjad.book.LilyPondBlock,
    abjad.book.LilyPondOutputProxy,
    abjad.book.RawLilyPondOutputProxy,
    abjad.book.RevealDirective,
    abjad.book.ShellDirective,
    abjad.book.ThumbnailDirective,
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
