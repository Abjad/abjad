# -*- encoding: utf-8 -*-
import inspect
import pickle
import pytest
import abjad
from abjad.tools import datastructuretools
from abjad.tools import documentationtools
from abjad.tools import lilypondparsertools
from abjad.tools import quantizationtools
from abjad.tools import rhythmmakertools
from abjad.tools import rhythmtreetools
from abjad.tools import selectiontools
from abjad.tools import systemtools
from abjad.tools import tonalanalysistools


_classes_to_fix = (
    documentationtools.ClassDocumenter,
    documentationtools.InheritanceGraph,
    documentationtools.Pipe,
    lilypondparsertools.LilyPondParser,
    lilypondparsertools.SchemeParser,
    lilypondparsertools.ReducedLyParser,
    quantizationtools.ParallelJobHandlerWorker,
    rhythmtreetools.RhythmTreeParser,
    selectiontools.ContiguousSelection,
    selectiontools.Descendants,
    selectiontools.LogicalTie,
    selectiontools.Lineage,
    selectiontools.Parentage,
    selectiontools.Selection,
    selectiontools.SimultaneousSelection,
    selectiontools.SliceSelection,
    selectiontools.VerticalMoment,
    systemtools.LilyPondFormatBundle,
    systemtools.LilyPondFormatBundle.SlotContributions,
    systemtools.RedirectedStreams,
    tonalanalysistools.TonalAnalysisAgent,
    tonalanalysistools.RootedChordClass
    )
_classes_with_generators = (
    rhythmmakertools.EvenDivisionRhythmMaker,
    )

classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test_abjad_pickle_01(class_):
    r'''All storage-formattable classes are pickable.
    '''

    if '_storage_format_specification' in dir(class_):
        if inspect.isabstract(class_):
            return
        if class_ in _classes_to_fix:
            return
        if class_ in _classes_with_generators:
            return
        instance_one = class_()
        pickle_string = pickle.dumps(instance_one)
        instance_two = pickle.loads(pickle_string)
        instance_one_format = format(instance_one, 'storage')
        instance_two_format = format(instance_two, 'storage')
        assert instance_one_format == instance_two_format