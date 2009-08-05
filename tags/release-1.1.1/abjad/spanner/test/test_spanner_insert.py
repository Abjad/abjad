from abjad import *


def test_spanner_insert_01( ):
   '''Insert component in spanner at index i.
      Add spanner to component's aggregator.
      Component then knows about spanner and vice versa.
      Not composer-safe.
      Inserting into middle of spanner may leave discontiguous spanner.'''

   t = Voice(construct.scale(4))
   p = Beam(t[:2])

   r'''\new Voice {
           c'8 [
           d'8 ]
           e'8
           f'8
   }'''

   p._insert(1, t.leaves[-1])

   "Interior insert leaves discontiguous spanner: Beam(c'8, f'8, d'8)."

   assert not check.wf(t)


def test_spanner_insert_02( ):
   '''Insert component at index zero in spanner.
      This operation does not mangle spanner.
      Operation is still not composer-safe, however.
      Note that p.append( ) and p.append_left( ) are composer-safe.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   p = Beam(t[1])

   r'''\new Voice {
      {
         c'8
         d'8
      }
      {
         e'8 [
         f'8 ]
      }
      {
         g'8
         a'8
      }
   }'''

   p._insert(0, t[0][1])

   r'''\new Voice {
      {
         c'8
         d'8 [
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

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8 [\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
