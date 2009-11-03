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


def test_formattools_report_03( ):
   '''You can report on tuplets.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   t.accidental.style = 'forget'
   t.bar_line.kind = '|.'
   t.clef.forced = Clef('treble')

   r'''
   \times 2/3 {
           #(set-accidental-style 'forget)
           \clef "treble"
           c'8
           d'8
           e'8
           \bar "|."
   }
   '''

   result = formattools.report(t, output = 'string')

   r'''
   slot_1
   slot_2
      BracketsInterface.open
         \times 2/3 {
   slot_3
      InterfaceAggregator.opening
            #(set-accidental-style 'forget)
            \clef "treble"
   slot_4
      _TupletFormatter._contents
            c'8
            d'8
            e'8
   slot_5
      InterfaceAggregator.closing
            \bar "|."
   slot_6
      BracketsInterface.close
         }
   slot_7
   '''

   assert result == 'slot_1\nslot_2\n\tBracketsInterface.open\n\t\t\\times 2/3 {\nslot_3\n\tInterfaceAggregator.opening\n\t\t\t#(set-accidental-style \'forget)\n\t\t\t\\clef "treble"\nslot_4\n\t_TupletFormatter._contents\n\t\t\tc\'8\n\t\t\td\'8\n\t\t\te\'8\nslot_5\n\tInterfaceAggregator.closing\n\t\t\t\\bar "|."\nslot_6\n\tBracketsInterface.close\n\t\t}\nslot_7\n'
