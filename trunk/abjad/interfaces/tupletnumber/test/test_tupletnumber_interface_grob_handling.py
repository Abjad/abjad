from abjad import *


def test_tupletnumber_interface_grob_handling_01( ):
   '''Abjad tuplets wrap grob overrides at before and after.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   t.tupletnumber.fraction = True

   r'''\override TupletNumber #'fraction = ##t
   \times 2/3 {
           c'8
           d'8
           e'8
   }
   \revert TupletNumber #'fraction'''

   assert check.wf(t)
   assert t.format == "\\override TupletNumber #'fraction = ##t\n\\times 2/3 {\n\tc'8\n\td'8\n\te'8\n}\n\\revert TupletNumber #'fraction"


def test_tupletnumber_interface_grob_handling_02( ):
   '''Override LilyPond TupletNumber grob on Abjad voice.'''

   t = Voice(construct.scale(4))
   Beam(t[:])
   t.tupletnumber.fraction = True

   r'''\new Voice \with {
           \override TupletNumber #'fraction = ##t
   } {
           c'8 [
           d'8
           e'8
           f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice \\with {\n\t\\override TupletNumber #'fraction = ##t\n} {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"

def test_tupletnumber_interface_grob_handling_03( ):
   '''Override LilyPond TupletNumber grob on Abjad leaf.'''

   t = Voice(construct.scale(4))
   Beam(t[:])
   t[1].tupletnumber.fraction = True

   r'''\new Voice {
           c'8 [
           \once \override TupletNumber #'fraction = ##t
           d'8
           e'8
           f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\t\\once \\override TupletNumber #'fraction = ##t\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_tupletnumber_interface_grob_handling_04( ):
   '''Override LilyPond TupletNumber text attribute.'''

   t = Voice(construct.scale(4))
   Beam(t[:])
   t.tupletnumber.text = Markup('"6:4"')

   r'''\new Voice \with {
           \override TupletNumber #'text = \markup { "6:4" }
   } {
           c'8 [
           d'8
           e'8
           f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == '\\new Voice \\with {\n\t\\override TupletNumber #\'text = \\markup { "6:4" }\n} {\n\tc\'8 [\n\td\'8\n\te\'8\n\tf\'8 ]\n}'
