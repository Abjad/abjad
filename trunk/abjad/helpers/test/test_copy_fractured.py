from abjad import *


def test_copy_fractured_01( ):
   '''Deep copy components in 'components'.
      Deep copy spanners that attach to any component in 'components'.
      Fracture spanners that attach to components not in 'components'.
      Return Python list of copied components.'''

   t = Voice(RigidMeasure((2, 8), run(2)) * 3)
   diatonicize(t)
   slur = Slur(t[:])
   trill = Trill(t.leaves)
   beam = Beam(t[0][:] + t[1:2] + t[2][:])

   r'''\new Voice {
         \time 2/8
         c'8 [ ( \startTrillSpan
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8 ] ) \stopTrillSpan
   }'''

   result = copy_fractured(t.leaves[2:4])
   new = Voice(result)

   r'''\new Voice {
      e'8 \startTrillSpan
      f'8 \stopTrillSpan
   }'''

   assert check(t)
   assert check(new)
   assert new.format == "\\new Voice {\n\te'8 \\startTrillSpan\n\tf'8 \\stopTrillSpan\n}"
   

def test_copy_fractured_02( ):
   '''Copy one measure and fracture spanners.'''

   t = Voice(RigidMeasure((2, 8), run(2)) * 3)
   diatonicize(t)
   slur = Slur(t[:])
   trill = Trill(t.leaves)
   beam = Beam(t[0][:] + t[1:2] + t[2][:])

   r'''\new Voice {
         \time 2/8
         c'8 [ ( \startTrillSpan
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8 ] ) \stopTrillSpan
   }'''

   result = copy_fractured(t[1:2])
   new = Voice(result)

   r'''\new Voice {
         \time 2/8
         e'8 [ ( \startTrillSpan
         f'8 ] ) \stopTrillSpan
   }'''

   assert check(t)
   assert check(new)
   assert new.format == "\\new Voice {\n\t\t\\time 2/8\n\t\te'8 [ ( \\startTrillSpan\n\t\tf'8 ] ) \\stopTrillSpan\n}"


def test_copy_fractured_03( ):
   '''Three notes crossing measure boundaries.'''

   t = Voice(RigidMeasure((2, 8), run(2)) * 3)
   diatonicize(t)
   slur = Slur(t[:])
   trill = Trill(t.leaves)
   beam = Beam(t[0][:] + t[1:2] + t[2][:])

   r'''\new Voice {
         \time 2/8
         c'8 [ ( \startTrillSpan
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8 ] ) \stopTrillSpan
   }'''

   result = copy_fractured(t.leaves[-3:])
   new = Voice(result)

   r'''\new Voice {
      f'8 \startTrillSpan
      g'8 [
      a'8 ] \stopTrillSpan
   }'''

   assert check(t)
   assert check(new)
   assert new.format == "\\new Voice {\n\tf'8 \\startTrillSpan\n\tg'8 [\n\ta'8 ] \\stopTrillSpan\n}"
