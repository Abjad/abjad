from abjad import *


def test_bequeath_multiple_01( ):
   
   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t[:])

   r'''
   \new Staff {
      c'8 [ \<
      d'8 ]
      e'8 [
      f'8 ] \!
   }
   '''

   new_notes = Note(12, (1, 16)) * 5
   bequeath_multiple(t[1:3], new_notes)

   r'''
   \new Staff {
      c'8 [ ] \<
      c''16
      c''16
      c''16
      c''16
      c''16
      f'8 [ ] \!
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 [ ] \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16\n\tc''16\n\tf'8 [ ] \\!\n}"


def test_bequeath_multiple_02( ):
   
   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t[:])

   r'''
   \new Staff {
      c'8 [ \<
      d'8 ]
      e'8 [
      f'8 ] \!
   }
   '''

   new_notes = Note(12, (1, 16)) * 5
   bequeath_multiple(t[:1], new_notes)

   r'''
   \new Staff {
      c''16 [ \<
      c''16
      c''16
      c''16
      c''16
      d'8 ]
      e'8 [
      f'8 ] \!
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc''16 [ \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16\n\td'8 ]\n\te'8 [\n\tf'8 ] \\!\n}"


def test_bequeath_multiple_03( ):

   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t[:])

   r'''
   \new Staff {
      c'8 [ \<
      d'8 ]
      e'8 [
      f'8 ] \!
   }
   '''

   new_notes = Note(12, (1, 16)) * 5
   bequeath_multiple(t[:2], new_notes)

   r'''
   \new Staff {
      c''16 [ \<
      c''16
      c''16
      c''16
      c''16 ]
      e'8 [
      f'8 ] \!
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc''16 [ \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16 ]\n\te'8 [\n\tf'8 ] \\!\n}"


def test_bequeath_multiple_04( ):

   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t[:])

   r'''
   \new Staff {
      c'8 [ \<
      d'8 ]
      e'8 [
      f'8 ] \!
   }
   '''

   new_notes = Note(12, (1, 16)) * 5
   bequeath_multiple(t[:3], new_notes)

   r'''
   \new Staff {
      c''16 \<
      c''16
      c''16
      c''16
      c''16
      f'8 [ ] \!
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc''16 \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16\n\tf'8 [ ] \\!\n}"


def test_bequeath_multiple_05( ):

   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t[:])

   r'''
   \new Staff {
      c'8 [ \<
      d'8 ]
      e'8 [
      f'8 ] \!
   }
   '''

   new_notes = Note(12, (1, 16)) * 5
   bequeath_multiple(t[:], new_notes)

   r'''
   \new Staff {
      c''16 \<
      c''16
      c''16
      c''16
      c''16 \!
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc''16 \\<\n\tc''16\n\tc''16\n\tc''16\n\tc''16 \\!\n}"
