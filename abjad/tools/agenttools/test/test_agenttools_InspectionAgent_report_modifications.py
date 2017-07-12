# -*- coding: utf-8 -*-
import abjad
import pytest


def test_agenttools_InspectionAgent_report_modifications_01():

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    comment = abjad.LilyPondComment('Example voice', 'before')
    abjad.attach(comment, voice)
    abjad.override(voice).note_head.color = 'red'
    command = abjad.LilyPondCommand("#(set-accidental-style 'forget)")
    abjad.attach(command, voice)
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    abjad.override(beam).beam.thickness = 3

    assert format(voice) == abjad.String.normalize(
        r'''
        % Example voice
        \new Voice \with {
            \override NoteHead.color = #red
        } {
            #(set-accidental-style 'forget)
            \override Beam.thickness = #3
            c'8 [
            d'8
            e'8
            \revert Beam.thickness
            f'8 ]
        }
        '''
        )

    result = abjad.inspect(voice).report_modifications()

    assert format(result) == abjad.String.normalize(
        r'''
        % Example voice
        \new Voice \with {
            \override NoteHead.color = #red
        } {
            #(set-accidental-style 'forget)
            %%% 4 components omitted %%%
        }
        '''
        )


def test_agenttools_InspectionAgent_report_modifications_02():

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    comment = abjad.LilyPondComment('Example tuplet', 'before')
    abjad.attach(comment, tuplet)
    abjad.override(tuplet).note_head.color = 'red'
    command = abjad.LilyPondCommand("#(set-accidental-style 'forget)")
    abjad.attach(command, tuplet)
    beam = abjad.Beam()
    abjad.attach(beam, tuplet[:])
    abjad.override(beam).beam.thickness = 3

    assert format(tuplet) == abjad.String.normalize(
        r'''
        % Example tuplet
        \override NoteHead.color = #red
        \times 2/3 {
            #(set-accidental-style 'forget)
            \override Beam.thickness = #3
            c'8 [
            d'8
            \revert Beam.thickness
            e'8 ]
        }
        \revert NoteHead.color
        '''
        )

    result = abjad.inspect(tuplet).report_modifications()

    assert format(result) == abjad.String.normalize(
        r'''
        % Example tuplet
        \override NoteHead.color = #red
        \times 2/3 {
            #(set-accidental-style 'forget)
            %%% 3 components omitted %%%
        }
        \revert NoteHead.color
        '''
        )
