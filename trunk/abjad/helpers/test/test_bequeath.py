from abjad import *


def test_bequeath_01( ):
   '''Bequeath parent and spanners of two old notes to five new notes.'''
   
   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t[:])

   r'''\new Staff {
      c'8 [ \<
      d'8 ]
      e'8 [
      f'8 ] \!
   }'''

   new_notes = Note(12, (1, 16)) * 5
   bequeath(t[1:3], new_notes)

   "Equivalent to t[1:3] = new_notes"

   r'''\new Staff {
      c'8 [ ] \<
      c''16
      c''16
      c''16
      c''16
      c''16
      f'8 [ ] \!
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 [ ] \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16\n\tc''16\n\tf'8 [ ] \\!\n}"


def test_bequeath_02( ):
   '''Bequeath parent and spaners of one old note to five new notes.'''
   
   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t[:])

   r'''\new Staff {
      c'8 [ \<
      d'8 ]
      e'8 [
      f'8 ] \!
   }'''

   new_notes = Note(12, (1, 16)) * 5
   bequeath(t[:1], new_notes)

   "Equivalent to t[:1] = new_notes."

   r'''\new Staff {
      c''16 [ \<
      c''16
      c''16
      c''16
      c''16
      d'8 ]
      e'8 [
      f'8 ] \!
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc''16 [ \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16\n\td'8 ]\n\te'8 [\n\tf'8 ] \\!\n}"


def test_bequeath_03( ):
   '''Bequeath parent and spanners of two old notes to five new notes.'''

   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t[:])

   r'''\new Staff {
      c'8 [ \<
      d'8 ]
      e'8 [
      f'8 ] \!
   }'''

   new_notes = Note(12, (1, 16)) * 5
   bequeath(t[:2], new_notes)

   "Equivalent to t[:2] = new_notes."

   r'''\new Staff {
      c''16 [ \<
      c''16
      c''16
      c''16
      c''16 ]
      e'8 [
      f'8 ] \!
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc''16 [ \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16 ]\n\te'8 [\n\tf'8 ] \\!\n}"


def test_bequeath_04( ):
   '''Bequeath parent and spanners of three old notes to five new notes.'''

   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t[:])

   r'''\new Staff {
      c'8 [ \<
      d'8 ]
      e'8 [
      f'8 ] \!
   }'''

   new_notes = Note(12, (1, 16)) * 5
   bequeath(t[:3], new_notes)

   "Equivalent to t[:3] = new_notes."

   r'''\new Staff {
      c''16 \<
      c''16
      c''16
      c''16
      c''16
      f'8 [ ] \!
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc''16 \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16\n\tf'8 [ ] \\!\n}"


def test_bequeath_05( ):

   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t[:])

   r'''\new Staff {
      c'8 [ \<
      d'8 ]
      e'8 [
      f'8 ] \!
   }'''

   new_notes = Note(12, (1, 16)) * 5
   bequeath(t[:], new_notes)

   "Equivalent to t[:] = new_notes."

   r'''\new Staff {
      c''16 \<
      c''16
      c''16
      c''16
      c''16 \!
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc''16 \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16 \\!\n}"


def test_bequeath_06( ):
   '''Bequeath parent and spanners of container to children of container.
      This is bequeath generalizing Container.slip( ).'''

   t = Staff([Voice(scale(4))])
   Beam(t[0])

   r'''\new Staff {
      \new Voice {
         c'8 [
         d'8
         e'8
         f'8 ]
      }
   }'''

   old_components = bequeath(t[0:1], t[0][:])
   voice = old_components[0]

   "Equivalent to t[:1] = t[0][:]."

   r'''\new Staff {
      c'8 [
      d'8
      e'8
      f'8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
   assert len(old_components) == 1
   assert len(voice) == 0
