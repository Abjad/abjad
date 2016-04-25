# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent_has_indicator_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    attach('foo', staff)

    assert inspect_(staff).has_indicator(str)
    assert not inspect_(staff[0]).has_indicator(str)
    assert not inspect_(staff[1]).has_indicator(str)
    assert not inspect_(staff[2]).has_indicator(str)
    assert not inspect_(staff[3]).has_indicator(str)


def test_agenttools_InspectionAgent_has_indicator_02():

    note = Note("c'4")
    assert not inspect_(note).has_indicator(indicatortools.IsAtSoundingPitch)

    attach(indicatortools.IsAtSoundingPitch(), note)
    assert inspect_(note).has_indicator(indicatortools.IsAtSoundingPitch)


def test_agenttools_InspectionAgent_has_indicator_03():

    staff = Staff("c'2 d'2")
    annotation = indicatortools.Annotation('name', 'value')
    attach(annotation, staff[0])

    assert inspect_(staff[0]).has_indicator(indicatortools.Annotation)
    assert not inspect_(staff[1]).has_indicator(indicatortools.Annotation)


def test_agenttools_InspectionAgent_has_indicator_04():

    staff = Staff("c'2 d'2")
    articulation = Articulation('staccato')
    attach(articulation, staff[0])

    assert inspect_(staff[0]).has_indicator(Articulation)
    assert not inspect_(staff[1]).has_indicator(Articulation)


def test_agenttools_InspectionAgent_has_indicator_05():

    staff = Staff("c'8 d'8 e'8 f'8")
    command = indicatortools.LilyPondCommand('break', 'closing')
    attach(command, staff[-1])

    assert not inspect_(staff[0]).has_indicator(indicatortools.LilyPondCommand)
    assert not inspect_(staff[1]).has_indicator(indicatortools.LilyPondCommand)
    assert not inspect_(staff[2]).has_indicator(indicatortools.LilyPondCommand)
    assert     inspect_(staff[3]).has_indicator(indicatortools.LilyPondCommand)


def test_agenttools_InspectionAgent_has_indicator_06():

    staff = Staff("c'2 d'2")
    comment = indicatortools.LilyPondComment('comment')
    attach(comment, staff[0])

    assert inspect_(staff[0]).has_indicator(indicatortools.LilyPondComment)
    assert not inspect_(staff[1]).has_indicator(indicatortools.LilyPondComment)


def test_agenttools_InspectionAgent_has_indicator_07():

    staff = Staff("c'2 d'2")
    stem_tremolo = indicatortools.StemTremolo(16)
    attach(stem_tremolo, staff[0])

    assert inspect_(staff[0]).has_indicator(indicatortools.StemTremolo)
    assert not inspect_(staff[1]).has_indicator(indicatortools.StemTremolo)


def test_agenttools_InspectionAgent_has_indicator_08():

    staff = Staff("c'8 d'8 e'8 f'8")
    time_signature = TimeSignature((4, 8))
    attach(time_signature, staff[0])

    assert inspect_(staff[0]).has_indicator(TimeSignature)
    assert not inspect_(staff[1]).has_indicator()
    assert not inspect_(staff[2]).has_indicator()
    assert not inspect_(staff[3]).has_indicator()
    assert not inspect_(staff).has_indicator()
