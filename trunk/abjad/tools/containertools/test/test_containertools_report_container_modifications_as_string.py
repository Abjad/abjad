from abjad import *
import py.test


def test_containertools_report_container_modifications_as_string_01():
    '''Context formatter report_container_modifications_as_string.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    marktools.LilyPondComment('Example voice', 'before')(t)
    t.override.note_head.color = 'red'
    marktools.LilyPondCommandMark("#(set-accidental-style 'forget)")(t)
    beam = spannertools.BeamSpanner(t[:])
    beam.override.beam.thickness = 3

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

    result = containertools.report_container_modifications_as_string(t)

    r'''
    % Example voice
    \new Voice \with {
        \override NoteHead #'color = #red
    } {
        #(set-accidental-style 'forget)

        %%% 4 components omitted %%%

    }
    '''

    assert result == "% Example voice\n\\new Voice \\with {\n\t\\override NoteHead #'color = #red\n} {\n\t#(set-accidental-style 'forget)\n\n\t%%% 4 components omitted %%%\n\n}"


def test_containertools_report_container_modifications_as_string_02():
    '''Tuplet formatter report_container_modifications_as_string.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    marktools.LilyPondComment('Example tuplet', 'before')(t)
    t.override.note_head.color = 'red'
    marktools.LilyPondCommandMark("#(set-accidental-style 'forget)")(t)
    beam = spannertools.BeamSpanner(t[:])
    beam.override.beam.thickness = 3

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

    result = containertools.report_container_modifications_as_string(t)

    r'''
    % Example tuplet
    \override NoteHead #'color = #red
    \times 2/3 {
        #(set-accidental-style 'forget)

        %%% 3 components omitted %%%

    }
    \revert NoteHead #'color
    '''

    assert result == "% Example tuplet\n\\override NoteHead #'color = #red\n\\times 2/3 {\n\t#(set-accidental-style 'forget)\n\n\t%%% 3 components omitted %%%\n\n}\n\\revert NoteHead #'color"
