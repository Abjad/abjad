# -*- encoding: utf-8 -*-
import inspect
import pytest
from abjad.tools import documentationtools
from abjad.tools import indicatortools
from abjad.tools import pitcharraytools
from abjad.tools import pitchtools
from abjad.tools import schemetools
from abjad.tools import tonalanalysistools


_allowed_to_be_empty_string = (
    indicatortools.Articulation,
    pitcharraytools.PitchArray,
    pitcharraytools.PitchArrayColumn,
    pitcharraytools.PitchArrayRow,
    pitchtools.Accidental,
    schemetools.SchemeColor,
    tonalanalysistools.ChordSuspension,
    )

classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___repr___01(class_):
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
