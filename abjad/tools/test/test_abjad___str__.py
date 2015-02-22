# -*- encoding: utf-8 -*-
import inspect
import pytest
from abjad import *


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
    datastructuretools.Enumeration,
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

    if not inspect.isabstract(class_):
        if not issubclass(class_, Exception):
            instance = class_()
            string = str(instance)
            assert string is not None
            if class_ not in _allowed_to_be_empty_string:
                assert string != ''