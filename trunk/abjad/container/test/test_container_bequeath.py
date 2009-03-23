from abjad import *
import py.test


def test_container_bequeath_01( ):
   '''Bequeath from sequential to voice.'''

   t = Voice(Sequential(run(2)) * 3)
   t.invocation.name = 'foo'
   diatonicize(t)
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

   old = t[1]

   r'''{
      e'8 \glissando
      f'8 \glissando
   }'''

   new = Voice( )
   new.invocation.name = 'foo'
   old.bequeath(new)

   assert t.format == '\\context Voice = "foo" {\n\t{\n\t\tc\'8 [ \\glissando\n\t\td\'8 \\glissando\n\t}\n\t\\context Voice = "foo" {\n\t\te\'8 \\glissando\n\t\tf\'8 \\glissando\n\t}\n\t{\n\t\tg\'8 \\glissando\n\t\ta\'8 ]\n\t}\n}'

   r'''\context Voice = "foo" {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      \new Voice {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }'''

   assert check(t)

   assert old.format == '{\n}'

   r'''{
   }'''

   assert new.format == '\\context Voice = "foo" {\n\te\'8 \\glissando\n\tf\'8 \\glissando\n}'

   r'''\context Voice = "foo" {
      e'8 \glissando
      f'8 \glissando
   }'''

   assert check(new)


def test_container_bequeath_02( ):
   '''Bequeath from sequential to tuplet.'''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
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

   t[1].bequeath(FixedDurationTuplet((3, 16), [ ]))

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

   assert check(t)


def test_container_bequeath_03( ):
   '''Bequeath from empty container to leaf.'''

   t = Voice([Sequential(scale(2)), Sequential([ ])])
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

   t[1].bequeath(Note(4, (1, 8)))

   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      e'8 ]
   }'''
   
   assert check(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\te'8 ]\n}"


def test_container_bequeath_04( ):
   '''Bequeath from empty container to nonempty container.'''

   t = Voice([Sequential(scale(2)), Sequential([ ])])
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

   sequential = Sequential([Note(4, (1, 8)), Note(5, (1, 8))])
   t[1].bequeath(sequential)

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

   assert check(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t{\n\t\te'8 \\glissando\n\t\tf'8 ]\n\t}\n}"
