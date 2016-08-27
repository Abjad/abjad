# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import rhythmmakertools
from abjad.tools import selectortools
from abjad.tools import systemtools


def test_systemtools_StorageFormatAgent_get_import_statements_01():
    subject = pitchtools.NamedPitch()
    agent = systemtools.StorageFormatAgent(subject)
    assert agent.get_import_statements() == (
        'from abjad.tools import pitchtools',
        )


def test_systemtools_StorageFormatAgent_get_import_statements_02():
    subject = selectortools.Selector().by_leaf()
    agent = systemtools.StorageFormatAgent(subject)
    assert agent.get_import_statements() == (
        'from abjad.tools import scoretools',
        'from abjad.tools import selectortools',
        )


def test_systemtools_StorageFormatAgent_get_import_statements_03():
    subject = [
        indicatortools.TimeSignature((3, 4)),
        indicatortools.TimeSignature((4, 4)),
        ]
    agent = systemtools.StorageFormatAgent(subject)
    assert agent.get_import_statements() == (
        'from abjad.tools import indicatortools',
        )


def test_systemtools_StorageFormatAgent_get_import_statements_04():
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
            simplify_redundant_tuplets=True,
            ),
        )
    agent = systemtools.StorageFormatAgent(subject)
    assert agent.get_import_statements() == (
        'from abjad.tools import durationtools',
        'from abjad.tools import mathtools',
        'from abjad.tools import rhythmmakertools',
        )
