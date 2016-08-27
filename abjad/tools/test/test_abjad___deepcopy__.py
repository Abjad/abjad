# -*- coding: utf-8 -*-
import copy
import inspect
import pytest
from abjad.tools import abjadbooktools
from abjad.tools import documentationtools
from abjad.tools import lilypondparsertools
from abjad.tools import quantizationtools
from abjad.tools import rhythmtreetools
from abjad.tools import scoretools
from abjad.tools import systemtools
from abjad.tools import tonalanalysistools


ignored_classes = (
    abjadbooktools.CodeBlock,
    abjadbooktools.CodeOutputProxy,
    abjadbooktools.GraphvizOutputProxy,
    abjadbooktools.LilyPondOutputProxy,
    lilypondparsertools.LilyPondParser,
    lilypondparsertools.ReducedLyParser,
    lilypondparsertools.SchemeParser,
    quantizationtools.ParallelJobHandlerWorker,
    rhythmtreetools.RhythmTreeParser,
    systemtools.RedirectedStreams,
    systemtools.StorageFormatAgent,
    systemtools.FormatSpecification,
    tonalanalysistools.RootedChordClass
    )

classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('class_', classes)
def test_abjad___deepcopy___01(class_):
    r'''All concrete classes with a storage format can copy.
    '''
    if (
        '_storage_format_specification' not in dir(class_) or
        '_get_format_specification' not in dir(class_)
        ):
        return
    if inspect.isabstract(class_):
        return
    instance_one = class_()
    instance_two = copy.deepcopy(instance_one)
    instance_one_format = format(instance_one, 'storage')
    instance_two_format = format(instance_two, 'storage')
    if not issubclass(class_, scoretools.Container):
        assert instance_one_format == instance_two_format
    # TODO: eventually this second asset should also pass
    #assert instance_one == instance_two
