# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_AttributeInspectionAgent_report_modifications_01():

    t = Voice("c'8 d'8 e'8 f'8")
    marktools.LilyPondComment('Example voice', 'before')(t)
    t.override.note_head.color = 'red'
    marktools.LilyPondCommandMark("#(set-accidental-style 'forget)")(t)
    beam = spannertools.BeamSpanner(t[:])
    beam.override.beam.thickness = 3

    assert testtools.compare(
        t,
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

    result = inspect(t).report_modifications()

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


def test_AttributeInspectionAgent_report_modifications_02():

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    marktools.LilyPondComment('Example tuplet', 'before')(t)
    t.override.note_head.color = 'red'
    marktools.LilyPondCommandMark("#(set-accidental-style 'forget)")(t)
    beam = spannertools.BeamSpanner(t[:])
    beam.override.beam.thickness = 3

    assert testtools.compare(
        t,
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

    result = inspect(t).report_modifications()

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
