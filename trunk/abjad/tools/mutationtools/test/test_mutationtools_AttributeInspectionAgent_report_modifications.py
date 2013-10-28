# -*- encoding: utf-8 -*-
import py.test
from abjad import *


def test_mutationtools_AttributeInspectionAgent_report_modifications_01():

    voice = Voice("c'8 d'8 e'8 f'8")
    comment = marktools.LilyPondComment('Example voice', 'before')
    comment.attach(voice)
    voice.override.note_head.color = 'red'
    command = marktools.LilyPondCommandMark("#(set-accidental-style 'forget)")
    command.attach(voice)
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:])
    beam.override.beam.thickness = 3

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

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    comment = marktools.LilyPondComment('Example tuplet', 'before')
    comment.attach(tuplet)
    tuplet.override.note_head.color = 'red'
    command = marktools.LilyPondCommandMark("#(set-accidental-style 'forget)")
    command.attach(tuplet)
    beam = spannertools.BeamSpanner()
    attach(beam, tuplet[:])
    beam.override.beam.thickness = 3

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
