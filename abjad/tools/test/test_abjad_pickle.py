import inspect
import pickle
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
    documentationtools.InheritanceGraph,
    lilypondparsertools.LilyPondParser,
    lilypondparsertools.SchemeParser,
    lilypondparsertools.ReducedLyParser,
    quantizationtools.ParallelJobHandlerWorker,
    rhythmtreetools.RhythmTreeParser,
    scoretools.Selection,
    scoretools.Descendants,
    scoretools.LogicalTie,
    scoretools.Lineage,
    scoretools.Parentage,
    scoretools.Selection,
    scoretools.Selection,
    scoretools.VerticalMoment,
    systemtools.LilyPondFormatBundle,
    systemtools.SlotContributions,
    systemtools.RedirectedStreams,
    systemtools.StorageFormatManager,
    systemtools.FormatSpecification,
    tonalanalysistools.TonalAnalysis,
    tonalanalysistools.RootedChordClass
    )

classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('class_', classes)
def test_abjad_pickle_01(class_):
    r'''All storage-formattable classes are pickable.
    '''
    if (
        '_get_storage_format_specification' not in dir(class_) or
        '_get_format_specification' not in dir(class_)
        ):
        return
    if inspect.isabstract(class_):
        return
    instance_one = class_()
    pickle_string = pickle.dumps(instance_one)
    instance_two = pickle.loads(pickle_string)
    instance_one_format = format(instance_one, 'storage')
    instance_two_format = format(instance_two, 'storage')
    assert instance_one_format == instance_two_format
