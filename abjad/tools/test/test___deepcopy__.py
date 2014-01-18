# -*- encoding: utf-8 -*-
import copy
import inspect
import pytest
import abjad
from abjad.tools import documentationtools
from abjad.tools import lilypondparsertools
from abjad.tools import quantizationtools
from abjad.tools import rhythmtreetools
from abjad.tools import scoretools


# TODO: make these work
_classes_to_fix = (
    documentationtools.ClassDocumenter,
    lilypondparsertools.LilyPondParser,
    lilypondparsertools.ReducedLyParser,
    lilypondparsertools.SchemeParser,
    quantizationtools.ParallelJobHandlerWorker,
    rhythmtreetools.RhythmTreeParser,
    )

classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___deepcopy___01(class_):
    r'''All concrete classes with a storage format can copy.
    '''

    if '_storage_format_specification' in dir(class_):
        if not inspect.isabstract(class_):
            if class_ not in _classes_to_fix:
                instance_one = class_()
                instance_two = copy.deepcopy(instance_one)
                instance_one_format = format(instance_one, 'storage')
                instance_two_format = format(instance_two, 'storage')
                if not issubclass(class_, scoretools.Container):
                    assert instance_one_format == instance_two_format
                # TODO: eventually this second asset should also pass
                #assert instance_one == instance_two
