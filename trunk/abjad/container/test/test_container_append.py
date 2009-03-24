from abjad import *
import py.test


def test_container_append_01( ):
   '''Append sequential to voice.'''

   t = Voice(run(2))
   Beam(t[:])
   t.append(Sequential(run(2)))
   diatonicize(t)

   r'''\new Voice {
           c'8 [
           d'8 ]
           {
                   e'8
                   f'8
           }
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\t{\n\t\te'8\n\t\tf'8\n\t}\n}"


def test_container_append_02( ):
   '''Append leaf to tuplet.'''

   t = FixedDurationTuplet((2, 8), scale(3))
   Beam(t[:])
   t.append(Note(5, (1, 16)))

   r'''\times 4/7 {
           c'8 [
           d'8
           e'8 ]
           f'16
   }'''

   assert check(t)
   assert t.format == "\\times 4/7 {\n\tc'8 [\n\td'8\n\te'8 ]\n\tf'16\n}"


def test_container_append_03( ):
   '''Trying to append noncomponent to container
      raises TypeError.'''

   t = Voice(scale(3))
   Beam(t[:])

   assert py.test.raises(TypeError, "t.append('foo')")
   assert py.test.raises(TypeError, "t.append(99)")
   assert py.test.raises(TypeError, "t.append([ ])")
   assert py.test.raises(TypeError, "t.append([Note(0, (1, 8))])")
