from abjad import *


def test_formattools_report_01( ):
   '''You can report on a heavily tweaked leaf.'''

   t = Note(0, (1, 4))
   t.notehead.style = 'cross'
   t.notehead.color = 'red'
   t.stem.color = 'red'
   t.articulations.append('staccato')
   t.articulations.append('tenuto')
   t.markup.down.append(r'\italic { ben. marcato }')
   t.comments.before.append('textual information before')
   t.comments.after.append('textual information after')

   assert formattools.report(t, output = 'string') == "slot_1\n\tCommentsInterface.before\n\t\t% textual information before\n\tInterfaceAggregator.overrides\n\t\t\\once \\override NoteHead #'color = #red\n\t\t\\once \\override NoteHead #'style = #'cross\n\t\t\\once \\override Stem #'color = #red\nslot_2\nslot_3\nslot_4\n\t_LeafFormatter._leaf_body\n\t\tc'4 -\\staccato -\\tenuto _ \\markup { \\italic { ben. marcato } }\nslot_5\nslot_6\nslot_7\n\tCommentsInterface.after\n\t\t% textual information after\n"


def test_formattools_report_02( ):
   '''You can report on spanners, too.'''

   t = Staff(construct.scale(4))
   spanner = Beam(t[2:])

   result = formattools.report(spanner, output = 'str')
   assert result == "e'8\tbefore: []\n\t after: []\n\t  left: []\n\t right: ['[']\n\nf'8\tbefore: []\n\t after: []\n\t  left: []\n\t right: [']']\n"
