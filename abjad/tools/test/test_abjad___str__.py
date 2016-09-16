# -*- coding: utf-8 -*-
import inspect
import pytest
from abjad.tools import abjadbooktools
from abjad.tools import datastructuretools
from abjad.tools import indicatortools
from abjad.tools import documentationtools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import schemetools
from abjad.tools import systemtools
from abjad.tools import tonalanalysistools


_allowed_to_be_empty_string = (
    indicatortools.Articulation,
    markuptools.Postscript,
    pitchtools.Accidental,
    pitchtools.PitchArray,
    pitchtools.PitchArrayColumn,
    pitchtools.PitchArrayRow,
    schemetools.SchemeColor,
    tonalanalysistools.ChordSuspension,
    )

ignored_classes = (
    abjadbooktools.AbjadDirective,
    abjadbooktools.CodeBlock,
    abjadbooktools.CodeOutputProxy,
    abjadbooktools.DoctestDirective,
    abjadbooktools.GraphvizOutputProxy,
    abjadbooktools.ImportDirective,
    abjadbooktools.LilyPondOutputProxy,
    abjadbooktools.RevealDirective,
    abjadbooktools.ShellDirective,
    abjadbooktools.ThumbnailDirective,
    datastructuretools.Enumeration,
    systemtools.StorageFormatAgent,
    systemtools.FormatSpecification,
    systemtools.TestCase,
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
