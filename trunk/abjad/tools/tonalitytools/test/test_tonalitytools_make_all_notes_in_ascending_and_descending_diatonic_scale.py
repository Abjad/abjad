from abjad import *
from abjad.tools import tonalitytools


def test_tonalitytools_make_all_notes_in_ascending_and_descending_diatonic_scale_01():

    score = tonalitytools.make_all_notes_in_ascending_and_descending_diatonic_scale(
        contexttools.KeySignatureMark('E', 'major'))

    r'''
    \new Score \with {
        tempoWholesPerMinute = #(ly:make-moment 30 1)
    } <<
        \new Staff {
            \key e \major
            e'8
            fs'8
            gs'8
            a'8
            b'8
            cs''8
            ds''8
            e''8
            ds''8
            cs''8
            b'8
            a'8
            gs'8
            fs'8
            e'4
        }
    >>
    '''

    assert score.format == "\\new Score \\with {\n\ttempoWholesPerMinute = #(ly:make-moment 30 1)\n} <<\n\t\\new Staff {\n\t\t\\key e \\major\n\t\te'8\n\t\tfs'8\n\t\tgs'8\n\t\ta'8\n\t\tb'8\n\t\tcs''8\n\t\tds''8\n\t\te''8\n\t\tds''8\n\t\tcs''8\n\t\tb'8\n\t\ta'8\n\t\tgs'8\n\t\tfs'8\n\t\te'4\n\t}\n>>"
