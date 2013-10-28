# -*- encoding: utf-8 -*-
from abjad import *


def test_formattools_report_component_format_contributions_01():
    r'''You can report_component_format_contributions on a heavily 
    tweaked leaf.
    '''

    t = Note("c'4")
    t.override.note_head.style = 'cross'
    t.override.note_head.color = 'red'
    t.override.stem.color = 'red'
    articulation = marktools.Articulation('staccato')
    attach(articulation, t)
    articulation = marktools.Articulation('tenuto')
    attach(articulation, t)
    markup = markuptools.Markup('some markup', Down)
    attach(markup, t)
    comment = marktools.LilyPondComment('textual information before', 'before')
    attach(comment, t)
    comment = marktools.LilyPondComment('textual information after', 'after')
    attach(comment, t)

    r'''
    slot 1:
        comments:
            % textual information before
        grob overrides:
            \once \override NoteHead #'color = #red
            \once \override NoteHead #'style = #'cross
            \once \override Stem #'color = #red
    slot 3:
    slot 4:
        leaf body:
            c'4 -\staccato -\tenuto _ \markup { some markup }
    slot 5:
    slot 7:
        comments:
            % textual information after
    '''

    assert formattools.report_component_format_contributions(t) == '''slot 1:\n\tcomments:\n\t\t% textual information before\n\tgrob overrides:\n\t\t\\once \\override NoteHead #'color = #red\n\t\t\\once \\override NoteHead #'style = #'cross\n\t\t\\once \\override Stem #'color = #red\nslot 3:\nslot 4:\n\tleaf body:\n\t\tc'4 -\\staccato -\\tenuto _ \\markup { some markup }\nslot 5:\nslot 7:\n\tcomments:\n\t\t% textual information after\n'''
