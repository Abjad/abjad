from abjad import *


def test_container_delitem_01( ):
   '''Delete 1 leaf in container. 
      Spanner structure is preserved.'''

   t = Voice(scale(4))
   Beam(t[:])

   del(t[1])

   r'''\new Voice {
           c'8 [
           e'8
           f'8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\te'8\n\tf'8 ]\n}"


def test_container_delitem_02( ):
   '''Delete slice in middle of container.'''

   t = Voice(scale(4))
   Beam(t[:])

   del(t[1:3])

   r'''\new Voice {
           c'8 [
           f'8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\tf'8 ]\n}"


def test_container_delitem_03( ):
   '''Delete slice from beginning to middle of container.'''

   t = Voice(scale(4))
   Beam(t[:])

   del(t[:2])

   r'''\new Voice {
           e'8 [
           f'8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\te'8 [\n\tf'8 ]\n}"


def test_container_delitem_04( ):
   '''Delete slice from middle to end of container.'''

   t = Voice(scale(4))
   Beam(t[:])

   del(t[2:])

   r'''\new Voice {
           c'8 [
           d'8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_container_delitem_05( ):
   '''Delete slice from beginning to end of container.'''

   t = Voice(scale(4)) 
   Beam(t[:])

   del(t[:])

   r'''\new Voice {
   }'''

   assert check(t)
   assert t.format == '\\new Voice {\n}'


def test_container_delitem_06( ):
   '''Detach leaf from tuplet and spanner.'''

   t = FixedDurationTuplet((2, 8), scale(3))
   Beam(t[:])

   del(t[1])

   r'''c'8 [
     e'8 ]'''

   assert check(t)
   assert t.format == "\tc'8 [\n\te'8 ]"
