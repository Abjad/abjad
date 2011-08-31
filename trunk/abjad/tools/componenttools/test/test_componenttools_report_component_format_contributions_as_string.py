from abjad import *
import py.test


def test_componenttools_report_component_format_contributions_as_string_01():
    '''You can report_component_format_contributions_as_string on a heavily tweaked leaf.'''

    t = Note("c'4")
    t.override.note_head.style = 'cross'
    t.override.note_head.color = 'red'
    t.override.stem.color = 'red'
    marktools.Articulation('staccato')(t)
    marktools.Articulation('tenuto')(t)
    markuptools.Markup(r'\italic { ben. marcato }', 'down')(t)
    marktools.LilyPondComment('textual information before', 'before')(t)
    marktools.LilyPondComment('textual information after', 'after')(t)

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
            c'4 -\staccato -\tenuto _ \markup { \italic { ben. marcato } }
    slot 5:
    slot 7:
        comments:
            % textual information after
    '''

    assert componenttools.report_component_format_contributions_as_string(t) == "slot 1:\n\tcomments:\n\t\t% textual information before\n\tgrob overrides:\n\t\t\\once \\override NoteHead #'color = #red\n\t\t\\once \\override NoteHead #'style = #'cross\n\t\t\\once \\override Stem #'color = #red\nslot 3:\nslot 4:\n\tleaf body:\n\t\tc'4 -\\staccato -\\tenuto _ \\markup { \\italic { ben. marcato } }\nslot 5:\nslot 7:\n\tcomments:\n\t\t% textual information after\n"
