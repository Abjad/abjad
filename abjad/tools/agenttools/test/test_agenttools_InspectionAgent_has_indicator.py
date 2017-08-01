# -*- coding: utf-8 -*-
import abjad


def test_agenttools_InspectionAgent_has_indicator_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.attach('foo', staff[0])

    assert not abjad.inspect(staff).has_indicator(str)
    assert abjad.inspect(staff[0]).has_indicator(str)
    assert not abjad.inspect(staff[1]).has_indicator(str)
    assert not abjad.inspect(staff[2]).has_indicator(str)
    assert not abjad.inspect(staff[3]).has_indicator(str)


def test_agenttools_InspectionAgent_has_indicator_02():

    staff = abjad.Staff("c'2 d'2")
    articulation = abjad.Articulation('staccato')
    abjad.attach(articulation, staff[0])

    assert abjad.inspect(staff[0]).has_indicator(abjad.Articulation)
    assert not abjad.inspect(staff[1]).has_indicator(abjad.Duration)


def test_agenttools_InspectionAgent_has_indicator_03():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    command = abjad.LilyPondCommand('break', 'closing')
    abjad.attach(command, staff[-1])

    assert not abjad.inspect(staff[0]).has_indicator(abjad.LilyPondCommand)
    assert not abjad.inspect(staff[1]).has_indicator(abjad.LilyPondCommand)
    assert not abjad.inspect(staff[2]).has_indicator(abjad.LilyPondCommand)
    assert     abjad.inspect(staff[3]).has_indicator(abjad.LilyPondCommand)


def test_agenttools_InspectionAgent_has_indicator_04():

    staff = abjad.Staff("c'2 d'2")
    comment = abjad.LilyPondComment('comment')
    abjad.attach(comment, staff[0])

    assert abjad.inspect(staff[0]).has_indicator(abjad.LilyPondComment)
    assert not abjad.inspect(staff[1]).has_indicator(abjad.LilyPondComment)


def test_agenttools_InspectionAgent_has_indicator_05():

    staff = abjad.Staff("c'2 d'2")
    stem_tremolo = abjad.StemTremolo(16)
    abjad.attach(stem_tremolo, staff[0])

    assert abjad.inspect(staff[0]).has_indicator(abjad.StemTremolo)
    assert not abjad.inspect(staff[1]).has_indicator(abjad.StemTremolo)


def test_agenttools_InspectionAgent_has_indicator_06():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    time_signature = abjad.TimeSignature((4, 8))
    abjad.attach(time_signature, staff[0])

    assert abjad.inspect(staff[0]).has_indicator(abjad.TimeSignature)
    assert not abjad.inspect(staff[1]).has_indicator()
    assert not abjad.inspect(staff[2]).has_indicator()
    assert not abjad.inspect(staff[3]).has_indicator()
    assert not abjad.inspect(staff).has_indicator()
