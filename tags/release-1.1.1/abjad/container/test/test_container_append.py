from abjad import *
import py.test


def test_container_append_01( ):
   '''Append sequential to voice.'''

   t = Voice(construct.run(2))
   Beam(t[:])
   t.append(Container(construct.run(2)))
   pitchtools.diatonicize(t)

   r'''\new Voice {
           c'8 [
           d'8 ]
           {
                   e'8
                   f'8
           }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\t{\n\t\te'8\n\t\tf'8\n\t}\n}"


def test_container_append_02( ):
   '''Append leaf to tuplet.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   Beam(t[:])
   t.append(Note(5, (1, 16)))

   r'''\times 4/7 {
           c'8 [
           d'8
           e'8 ]
           f'16
   }'''

   assert check.wf(t)
   assert t.format == "\\times 4/7 {\n\tc'8 [\n\td'8\n\te'8 ]\n\tf'16\n}"


def test_container_append_03( ):
   '''Trying to append noncomponent to container
      raises TypeError.'''

   t = Voice(construct.scale(3))
   Beam(t[:])

   assert py.test.raises(TypeError, "t.append('foo')")
   assert py.test.raises(TypeError, "t.append(99)")
   assert py.test.raises(TypeError, "t.append([ ])")
   assert py.test.raises(TypeError, "t.append([Note(0, (1, 8))])")


def test_container_append_04( ):
   '''Append spanned leaf from donor container to recipient container.'''

   t = Voice(construct.scale(3))
   Beam(t[:])

   r'''\new Voice {
      c'8 [
      d'8
      e'8 ]
   }'''

   u = Voice(construct.scale(4))
   Beam(u[:])

   r'''\new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }'''

   t.append(u[-1])

   "Container t is now ..."

   r'''\new Voice {
      c'8 [
      d'8
      e'8 ]
      f'8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8 ]\n\tf'8\n}"

   "Container u is now ..."

   r'''\new Voice {
      c'8 [
      d'8
      e'8 ]
   }'''

   assert check.wf(u)
   assert u.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8 ]\n}"


def test_container_append_05( ):
   '''Append spanned leaf from donor container to recipient container.
      Donor and recipient containers are the same.'''

   t = Voice(construct.scale(4))
   Beam(t[:])

   r'''\new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }'''

   t.append(t[1])

   r'''\new Voice {
      c'8 [
      e'8
      f'8 ]
      d'8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\te'8\n\tf'8 ]\n\td'8\n}"
