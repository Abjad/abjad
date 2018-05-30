import copy
import inspect
import pytest
from abjad.tools import documentationtools
from abjad.tools import lilypondparsertools
from abjad.tools import rhythmtreetools
from abjad.tools import scoretools
from abjad.tools import systemtools
from abjad import tonalanalysis


ignored_classes = (
    lilypondparsertools.LilyPondParser,
    lilypondparsertools.ReducedLyParser,
    lilypondparsertools.SchemeParser,
    rhythmtreetools.RhythmTreeParser,
    systemtools.RedirectedStreams,
    systemtools.StorageFormatManager,
    systemtools.FormatSpecification,
    tonalanalysis.RootedChordClass
    )

classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('class_', classes)
def test_abjad___deepcopy___01(class_):
    r'''All concrete classes with a storage format can copy.
    '''
    if (
        '_get_storage_format_specification' not in dir(class_) or
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
