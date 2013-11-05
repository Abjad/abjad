# -*- encoding: utf-8 -*-
import py.test
from abjad import *


def test_mutationtools_AttributeInspectionAgent_report_modifications_01():

    voice = Voice("c'8 d'8 e'8 f'8")
    comment = marktools.LilyPondComment('Example voice', 'before')
    attach(comment, voice)
    override(voice).note_head.color = 'red'
    command = marktools.LilyPondCommandMark("#(set-accidental-style 'forget)")
    attach(command, voice)
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:])
    override(beam).beam.thickness = 3

    assert testtools.compare(
        voice,
        r'''
        % Example voice
        \new Voice \with {
            \override NoteHead #'color = #red
        } {
            #(set-accidental-style 'forget)
            \override Beam #'thickness = #3
            c'8 [
            d'8
            e'8
            f'8 ]
            \revert Beam #'thickness
        }
        '''
        )

    result = inspect(voice).report_modifications()

    assert testtools.compare(
        result,
        r'''
        % Example voice
        \new Voice \with {
            \override NoteHead #'color = #red
        } {
            #(set-accidental-style 'forget)
            %%% 4 components omitted %%%
        }
        '''
        )


def test_mutationtools_AttributeInspectionAgent_report_modifications_02():

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    comment = marktools.LilyPondComment('Example tuplet', 'before')
    attach(comment, tuplet)
    override(tuplet).note_head.color = 'red'
    command = marktools.LilyPondCommandMark("#(set-accidental-style 'forget)")
    attach(command, tuplet)
    beam = spannertools.BeamSpanner()
    attach(beam, tuplet[:])
    override(beam).beam.thickness = 3

    assert testtools.compare(
        tuplet,
        r'''
        % Example tuplet
        \override NoteHead #'color = #red
        \times 2/3 {
            #(set-accidental-style 'forget)
            \override Beam #'thickness = #3
            c'8 [
            d'8
            e'8 ]
            \revert Beam #'thickness
        }
        \revert NoteHead #'color
        '''
        )

    result = inspect(tuplet).report_modifications()

    assert testtools.compare(
        result,
        r'''
        % Example tuplet
        \override NoteHead #'color = #red
        \times 2/3 {
            #(set-accidental-style 'forget)
            %%% 3 components omitted %%%
        }
        \revert NoteHead #'color
        '''
        )
