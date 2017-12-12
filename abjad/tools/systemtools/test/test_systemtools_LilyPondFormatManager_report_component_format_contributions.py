import abjad
from abjad.tools import systemtools


def test_systemtools_LilyPondFormatManager_report_component_format_contributions_01():
    r'''You can report_component_format_contributions on a heavily
    tweaked leaf.
    '''

    note = abjad.Note("c'4")
    abjad.override(note).note_head.style = 'cross'
    abjad.override(note).note_head.color = 'red'
    abjad.override(note).stem.color = 'red'
    articulation = abjad.Articulation('staccato')
    abjad.attach(articulation, note)
    articulation = abjad.Articulation('tenuto')
    abjad.attach(articulation, note)
    markup = abjad.Markup('some markup', abjad.Down)
    abjad.attach(markup, note)
    comment = abjad.LilyPondComment('textual information before', 'before')
    abjad.attach(comment, note)
    comment = abjad.LilyPondComment('textual information after', 'after')
    abjad.attach(comment, note)

    assert systemtools.LilyPondFormatManager.report_component_format_contributions(note) == \
        abjad.String.normalize(
        r'''
        slot 1:
            comments:
                % textual information before
            grob overrides:
                \once \override NoteHead.color = #red
                \once \override NoteHead.style = #'cross
                \once \override Stem.color = #red
        slot 3:
        slot 4:
            leaf body:
                c'4 -\staccato -\tenuto _ \markup { "some markup" }
        slot 5:
        slot 7:
            comments:
                % textual information after
        ''')
