from abjad import *


def test_clone_unspan_01( ):
   '''Withdraw components from spanners.
      Deepcopy unspanned components.
      Reapply spanners to components.
      Return unspanned copy.'''

   t = Voice(RigidMeasure((2, 8), run(2)) * 4)
   diatonicize(t)
   beam = Beam(t[:2] + t[2][:] + t[3][:])
   slur = Slur(t[0][:] + t[1][:] + t[2:])

   r'''\new Voice {
         \time 2/8
         c'8 [ (
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8 ] )
   }'''

   result = clone.unspan([t])
   voice = result[0]

   r'''
   \new Voice {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8
   }'''

   assert check(t)
   assert check(voice)
   assert voice.format == "\\new Voice {\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t\t\\time 2/8\n\t\tb'8\n\t\tc''8\n}"
   

def test_clone_unspan_02( ):
   '''Withdraw components from spanners.
      Deepcopy unspanned components.
      Reapply spanners to components.
      Return unspanned copy.'''

   t = Voice(RigidMeasure((2, 8), run(2)) * 4)
   diatonicize(t)
   beam = Beam(t[:2] + t[2][:] + t[3][:])
   slur = Slur(t[0][:] + t[1][:] + t[2:])

   r'''\new Voice {
         \time 2/8
         c'8 [ (
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8 ] )
   }'''

   result = clone.unspan(t[1:])
   new = Voice(result)

   r'''\new Voice {
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8
   }'''

   assert check(t)
   assert check(new)
   assert new.format == "\\new Voice {\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t\t\\time 2/8\n\t\tb'8\n\t\tc''8\n}"


def test_clone_unspan_03( ):
   '''Withdraw components from spanners.
      Deepcopy unspanned components.
      Reapply spanners to components.
      Return unspanned copy.'''

   t = Voice(RigidMeasure((2, 8), run(2)) * 4)
   diatonicize(t)
   beam = Beam(t[:2] + t[2][:] + t[3][:])
   slur = Slur(t[0][:] + t[1][:] + t[2:])

   r'''\new Voice {
         \time 2/8
         c'8 [ (
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8 ] )
   }'''

   result = clone.unspan(t.leaves[:6])
   new = Voice(result)

   r'''\new Voice {
      c'8
      d'8
      e'8
      f'8
      g'8
      a'8
   }'''

   assert check(t)
   assert check(new)
   assert new.format == "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n}"


def test_clone_unspan_04( ):
   '''Withdraw components from spanners.
      Deepcopy unspanned components.
      Reapply spanners to components.
      Return unspanned copy.'''

   t = Voice(RigidMeasure((2, 8), run(2)) * 4)
   diatonicize(t)
   beam = Beam(t[:2] + t[2][:] + t[3][:])
   slur = Slur(t[0][:] + t[1][:] + t[2:])

   r'''\new Voice {
         \time 2/8
         c'8 [ (
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8 ] )
   }'''

   result = clone.unspan(t[2][:] + t[-1:])
   new = Voice(result)

   r'''\new Voice {
      g'8
      a'8
         \time 2/8
         b'8
         c''8
   }'''

   assert check(t)
   assert check(new)
   assert new.format == "\\new Voice {\n\tg'8\n\ta'8\n\t\t\\time 2/8\n\t\tb'8\n\t\tc''8\n}"


def test_clone_unspan_05( ):
   '''Withdraw components from spanners.
      Deepcopy unspanned components.
      Reapply spanners to components.
      Return unspanned copy.
      Use optional 'n' argument for multiple copies.'''

   t = Voice(RigidMeasure((2, 8), run(2)) * 4)
   diatonicize(t)
   beam = Beam(t[:2] + t[2][:] + t[3][:])
   slur = Slur(t[0][:] + t[1][:] + t[2:])

   r'''\new Voice {
         \time 2/8
         c'8 [ (
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8 ] )
   }'''

   result = clone.unspan(t[-2:], 3)
   new = Voice(result)

   r'''\new Voice {
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'8\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t\t\\time 2/8\n\t\tb'8\n\t\tc''8 ] )\n}"
