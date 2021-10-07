import inspect
import pickle

import pytest

import abjad

ignored_classes = (
    abjad.parsers.parser.LilyPondParser,
    abjad.parsers.reduced.ReducedLyParser,
    abjad.parsers.scheme.SchemeParser,
    abjad.Selection,
    abjad.Descendants,
    abjad.LogicalTie,
    abjad.Lineage,
    abjad.Parentage,
    abjad.Selection,
    abjad.Selection,
    abjad.rhythmtrees.RhythmTreeParser,
    abjad.VerticalMoment,
    abjad.LilyPondFormatBundle,
    abjad.SlotContributions,
    abjad.RedirectedStreams,
    abjad.FormatSpecification,
)

classes = abjad.list_all_classes(ignored_classes=ignored_classes)


@pytest.mark.parametrize("class_", classes)
def test_abjad_pickle_01(class_):
    """
    All storage-formattable classes are pickable.
    """
    if "_get_storage_format_specification" not in dir(
        class_
    ) or "_get_format_specification" not in dir(class_):
        return
    if inspect.isabstract(class_):
        return
    instance_one = class_()
    pickle_string = pickle.dumps(instance_one)
    instance_two = pickle.loads(pickle_string)
    instance_one_format = abjad.lilypond(instance_one, "storage")
    instance_two_format = abjad.lilypond(instance_two, "storage")
    assert instance_one_format == instance_two_format
