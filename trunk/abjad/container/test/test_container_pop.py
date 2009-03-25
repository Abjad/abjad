from abjad import *


def test_container_pop_01( ):
   '''Containers pop leaves correctly.
      Popped leaves detach from parent.
      Popped leaves withdraw from crossing spanners.
      Popped leaves carry covered spanners forward.'''

   t = Voice(scale(4))
   Slur(t[:])
   Beam(t[1])

   r'''\new Voice {
      c'8 (
      d'8 [ ]
      e'8
      f'8 )
   }'''

   result = t.pop(1)

   r''' \new Voice {
      c'8 (
      e'8
      f'8 )
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 (\n\te'8\n\tf'8 )\n}"

   "Result is now d'8 [ ]"

   assert check(result)
   assert result.format == "d'8 [ ]"


def test_container_pop_02( ):
   '''Containers pop nested containers correctly.
      Popped containers detach from both parent and spanners.'''

   t = Staff(Sequential(run(2)) * 2)
   diatonicize(t)
   p = Beam(t[:])

   r'''\new Staff {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8 ]
      }
   }'''

   sequential = t.pop( )

   r'''\new Staff {
      {
         c'8 [
         d'8 ]
      }
   }'''

   assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n}"
   assert check(t)

   r'''{
      e'8
      f'8
   }'''

   assert sequential.format == "{\n\te'8\n\tf'8\n}"
   assert check(sequential)
