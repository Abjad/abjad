from abjad import *


def test_spanner_remove_01( ):
   '''Remove interior component from spanner.
      Remove spanner from component's aggregator.
      Spanner is left discontiguous and score no longer checks.
      Not composer-safe. 
      Follow immediately with operation to remove component from score.'''

   t = Voice(scale(4))
   pitchtools.diatonicize(t)
   p = Beam(t[:])
   
   r'''\new Voice {
           c'8 [
           d'8
           e'8
           f'8 ]
   }'''

   p._remove(p.components[1])

   "Spanner is now discontiguous: Beam(c'8, e'8, f'8)."

   r'''\new Voice {
           c'8 [
           d'8
           e'8
           f'8 ]
   }'''

   assert not check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
   

def test_spanner_remove_02( ):
   '''Remove last component from spanner.
      Remove spanner from component's aggregator.
      Here an end element removes from spanner.
      So spanner is not left discontiguous and score checks.
      Still not composer-safe.
      Note spanner.pop( ) and spanner.pop_left( ) are composer-safe.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   p = Beam(t[:])
   
   r'''\new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }'''

   result = p._remove(p.components[2])

   r'''\new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8 ]
      }
      {
         g'8
         a'8
      }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
