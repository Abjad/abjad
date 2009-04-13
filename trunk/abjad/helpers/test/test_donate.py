from abjad import *
import py.test


def test_donate_09( ):
   '''Donate from multiple containers to tuplet.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   Beam(t.leaves)

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

   tuplet = FixedDurationTuplet((3, 8), [ ])
   donate(t[:2], tuplet)

   r'''\new Voice {
      \fraction \times 3/4 {
         c'8 [
         d'8
         e'8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\\fraction \\times 3/4 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"


def test_donate_02( ):
   '''Donate from container to voice.'''

   t = Voice(Container(construct.run(2)) * 3)
   t.name = 'foo'
   pitchtools.diatonicize(t)
   Glissando(t[:])
   Beam(t.leaves)
   
   r'''\context Voice = "foo" {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }'''

   new = Voice( )
   new.name = 'foo'
   donate(t[1:2], new)

   r'''\context Voice = "foo" {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      \context Voice = "foo" {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }'''

   assert check.wf(t)
   assert t.format == '\\context Voice = "foo" {\n\t{\n\t\tc\'8 [ \\glissando\n\t\td\'8 \\glissando\n\t}\n\t\\context Voice = "foo" {\n\t\te\'8 \\glissando\n\t\tf\'8 \\glissando\n\t}\n\t{\n\t\tg\'8 \\glissando\n\t\ta\'8 ]\n\t}\n}'


def test_donate_03( ):
   '''Donate from container to tuplet.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   Glissando(t[:])
   Beam(t.leaves)
   
   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }'''

   donate(t[1:2], FixedDurationTuplet((3, 16), [ ]))

   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      \fraction \times 3/4 {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }'''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t\\fraction \\times 3/4 {\n\t\te'8 \\glissando\n\t\tf'8 \\glissando\n\t}\n\t{\n\t\tg'8 \\glissando\n\t\ta'8 ]\n\t}\n}"

   assert check.wf(t)


def test_donate_04( ):
   '''Donate from empty container to leaf.'''

   t = Voice([Container(construct.scale(2)), Container([ ])])
   Glissando(t[:])
   Beam(t[:])

   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 ]
      }
      {
      }
   }'''

   donate(t[1:2], Note(4, (1, 8)))

   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      e'8 ]
   }'''
   
   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\te'8 ]\n}"


def test_donate_05( ):
   '''Donate from empty container to nonempty container.'''

   t = Voice([Container(construct.scale(2)), Container([ ])])
   Glissando(t[:])
   Beam(t[:])

   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 ]
      }
      {
      }
   }'''

   container = Container([Note(4, (1, 8)), Note(5, (1, 8))])
   donate(t[1:2], container)

   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 ]
      }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t{\n\t\te'8 \\glissando\n\t\tf'8 ]\n\t}\n}"


def test_donate_06( ):
   '''Trying to bequeath from nonempty container 
      to leaf raises MusicContentsError.'''

   t = Voice(Container(construct.run(2)) * 2)
   Beam(t[:])
   pitchtools.diatonicize(t)

   assert py.test.raises(MusicContentsError, 'donate(t[1:2], Note(4, (1, 4)))')


def test_donate_07( ):
   '''Trying to bequeath from nonempty container to 
      nonempty container raises MusicContentsError.'''
   
   t = Voice(Container(construct.run(2)) * 2)
   Beam(t[:])
   pitchtools.diatonicize(t)

   tuplet = FixedDurationTuplet((2, 8), construct.scale(3))
   assert py.test.raises(MusicContentsError, 'donate(t[1:2], tuplet)')


def test_donate_08( ):
   '''Donate from note to rest.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   Beam(t.leaves)   

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

   old = t.leaves[2]
   donate(t.leaves[2:3], Rest((1, 8)))

   r'''\new Voice {
      {
         c'8 [
         d'8
      }
      {
         r8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\tr8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"


def test_donate_09( ):
   '''Donate from note to tuplet.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   Glissando(t[:])
   Beam(t.leaves)   

   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }'''
   
   donate(t[1][:1], FixedDurationTuplet((1, 8), Note(0, (1, 16)) * 3))

   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         \times 2/3 {
            c'16 \glissando
            c'16 \glissando
            c'16 \glissando
         }
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t{\n\t\t\\times 2/3 {\n\t\t\tc'16 \\glissando\n\t\t\tc'16 \\glissando\n\t\t\tc'16 \\glissando\n\t\t}\n\t\tf'8 \\glissando\n\t}\n\t{\n\t\tg'8 \\glissando\n\t\ta'8 ]\n\t}\n}"


def test_donate_10( ):
   '''Donors that are not parent-contiguous raise ContiguityError.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   Beam(t.leaves)

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

   tuplet = FixedDurationTuplet((3, 8), [ ])
   assert py.test.raises(ContiguityError, 'donate([t[0], t[2]], tuplet)')
