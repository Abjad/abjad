# -*- encoding: utf-8 -*-
from abjad import *

manager = systemtools.StorageFormatManager


def test_systemtools_StorageFormatManager_get_import_statements_01():
    subject = pitchtools.NamedPitch()
    assert manager.get_import_statements(subject) == (
        'from abjad.tools import pitchtools',
        )


def test_systemtools_StorageFormatManager_get_import_statements_02():
    subject = selectortools.Selector().by_leaves()
    assert manager.get_import_statements(subject) == (
        'from abjad.tools import scoretools',
        'from abjad.tools import selectortools',
        )


def test_systemtools_StorageFormatManager_get_import_statements_03():
    subject = [TimeSignature((3, 4)), TimeSignature((4, 4))]
    assert manager.get_import_statements(subject) == (
        'from abjad.tools import indicatortools',
        )


def test_systemtools_StorageFormatManager_get_import_statements_04():
    subject = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=rhythmmakertools.InciseSpecifier(
            prefix_talea=(1,),
            prefix_counts=(0,),
            suffix_talea=(1,),
            suffix_counts=(1,),
            talea_denominator=16,
            body_ratio=mathtools.Ratio((1,)),
            outer_divisions_only=True,
            ),
        beam_specifier=rhythmmakertools.BeamSpecifier(
            beam_each_division=False,
            beam_divisions_together=False,
            ),
        duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
            decrease_durations_monotonically=True,
            forbidden_written_duration=durationtools.Duration(1, 2),
            ),
        tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
            avoid_dots=True,
            is_diminution=True,
            simplify_tuplets=True,
            ),
        )
    assert manager.get_import_statements(subject) == (
        'from abjad.tools import durationtools',
        'from abjad.tools import mathtools',
        'from abjad.tools import rhythmmakertools',
        )