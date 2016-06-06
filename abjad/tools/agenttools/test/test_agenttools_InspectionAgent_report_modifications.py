# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_agenttools_InspectionAgent_report_modifications_01():

    voice = Voice("c'8 d'8 e'8 f'8")
    comment = indicatortools.LilyPondComment('Example voice', 'before')
    attach(comment, voice)
    override(voice).note_head.color = 'red'
    command = indicatortools.LilyPondCommand("#(set-accidental-style 'forget)")
    attach(command, voice)
    beam = Beam()
    attach(beam, voice[:])
    override(beam).beam.thickness = 3

    assert format(voice) == stringtools.normalize(
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
            f'8 ]
            \revert Beam.thickness
        }
        '''
        )

    result = inspect_(voice).report_modifications()

    assert format(result) == stringtools.normalize(
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

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    comment = indicatortools.LilyPondComment('Example tuplet', 'before')
    attach(comment, tuplet)
    override(tuplet).note_head.color = 'red'
    command = indicatortools.LilyPondCommand("#(set-accidental-style 'forget)")
    attach(command, tuplet)
    beam = Beam()
    attach(beam, tuplet[:])
    override(beam).beam.thickness = 3

    assert format(tuplet) == stringtools.normalize(
        r'''
        % Example tuplet
        \override NoteHead.color = #red
        \times 2/3 {
            #(set-accidental-style 'forget)
            \override Beam.thickness = #3
            c'8 [
            d'8
            e'8 ]
            \revert Beam.thickness
        }
        \revert NoteHead.color
        '''
        )

    result = inspect_(tuplet).report_modifications()

    assert format(result) == stringtools.normalize(
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
