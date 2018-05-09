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
    abjad.book.AbjadDirective,
    abjad.book.CodeBlock,
    abjad.book.CodeOutputProxy,
    abjad.book.AbjadDoctestDirective,
    abjad.book.GraphvizOutputProxy,
    abjad.book.ImageOutputProxy,
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
def test_abjad___hash___01(class_):
    r'''All concrete classes with __hash__ can hash.
    '''
    if inspect.isabstract(class_):
        return
    if getattr(class_, '__hash__', None) is None:
        return
    instance = class_()
    value = hash(instance)
    assert isinstance(value, int)
