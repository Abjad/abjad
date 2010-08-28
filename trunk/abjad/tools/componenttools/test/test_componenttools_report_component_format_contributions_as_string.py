from abjad import *


def test_componenttools_report_component_format_contributions_as_string_01( ):
   '''You can report_component_format_contributions_as_string on a heavily tweaked leaf.'''

   t = Note(0, (1, 4))
   t.override.note_head.style = 'cross'
   t.override.note_head.color = 'red'
   t.override.stem.color = 'red'
   t.articulations.append('staccato')
   t.articulations.append('tenuto')
   t.markup.down.append(r'\italic { ben. marcato }')
   t.comments.before.append('textual information before')
   t.comments.after.append('textual information after')

   assert componenttools.report_component_format_contributions_as_string(t) == "slot_1\n\tCommentsInterface.before\n\t\t% textual information before\n\toverrides.overrides\n\t\t\\once \\override NoteHead #'color = #red\n\t\t\\once \\override NoteHead #'style = #'cross\n\t\t\\once \\override Stem #'color = #red\nslot_2\nslot_3\nslot_4\n\t_LeafFormatter._leaf_body\n\t\tc'4 -\\staccato -\\tenuto _ \\markup { \\italic { ben. marcato } }\nslot_5\nslot_6\nslot_7\n\tCommentsInterface.after\n\t\t% textual information after\n"


def test_componenttools_report_component_format_contributions_as_string_02( ):
   '''You can report on spanners, too.'''

   t = Staff(macros.scale(4))
   spanner = spannertools.BeamSpanner(t[2:])

   result = componenttools.report_component_format_contributions_as_string(spanner)
   assert result == "e'8\tbefore: []\n\t after: []\n\t  left: []\n\t right: ['[']\n\nf'8\tbefore: []\n\t after: []\n\t  left: []\n\t right: [']']\n"


def test_componenttools_report_component_format_contributions_as_string_03( ):
   '''You can report_component_format_contributions_as_string on tuplets.
   '''

   t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
   t.misc.set_accidental_style = 'forget'
   t.misc.bar = '|.'
   staff = Staff([t])
   marktools.ClefMark('treble')(t)

   r'''
   \new Staff {
      \times 2/3 {
         #(set-accidental-style 'forget)
         \clef "treble"
         c'8
         d'8
         e'8
         \bar "|."
      }
   }
   '''


   result = componenttools.report_component_format_contributions_as_string(t)

   r'''
   slot_1
   slot_2
      tuplet_brackets.open
         \times 2/3 {
   slot_3
      opening.opening
            #(set-accidental-style 'forget)
   slot_4
      _TupletFormatter._contents
            \clef "treble"
            c'8
            d'8
            e'8
   slot_5
      closing.closing
            \bar "|."
   slot_6
      tuplet_brackets.close
         }
   slot_7
   '''

   assert result == 'slot_1\nslot_2\n\ttuplet_brackets.open\n\t\t\\times 2/3 {\nslot_3\n\topening.opening\n\t\t\t#(set-accidental-style \'forget)\nslot_4\n\t_TupletFormatter._contents\n\t\t\t\\clef "treble"\n\t\t\tc\'8\n\t\t\td\'8\n\t\t\te\'8\nslot_5\n\tclosing.closing\n\t\t\t\\bar "|."\nslot_6\n\ttuplet_brackets.close\n\t\t}\nslot_7\n'
