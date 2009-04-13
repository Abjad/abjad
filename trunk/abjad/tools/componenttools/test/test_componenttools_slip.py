from abjad import *


def test_componenttools_slip_01( ):
   '''Containers can 'slip out' of score structure.'''

   t = Staff(Container(construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   p = Beam(t.leaves)

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

   sequential = t[0]
   componenttools.slip(t[0:1])

   r'''\new Staff {
           c'8 [
           d'8
           {
                   e'8
                   f'8 ]
           }
   }'''
   
   assert check.wf(t)
   assert len(sequential) == 0
   assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_componenttools_slip_02( ):
   '''Slip leaf from parentage and spanners.'''

   t = Voice(construct.scale(4))
   Beam(t[:])
   Glissando(t[:])
  
   note = t[1]
   componenttools.slip([note])

   r'''\new Voice {
      c'8 [ \glissando
      e'8 \glissando
      f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [ \\glissando\n\te'8 \\glissando\n\tf'8 ]\n}"


def test_componenttools_slip_03( ):
   '''Slip multiple leaves.'''

   t = Voice(construct.scale(4))
   Beam(t[:])
   Glissando(t[:])

   r'''\new Voice {
      c'8 [ \glissando
      d'8 \glissando
      e'8 \glissando
      f'8 ]
   }'''

   componenttools.slip(t[:2])

   r'''\new Voice {
      e'8 [ \glissando
      f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\te'8 [ \\glissando\n\tf'8 ]\n}"


def test_componenttools_slip_04( ):
   '''Slip multiple containers.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   Beam(t.leaves)
   Glissando(t.leaves)
   
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

   componenttools.slip(t[:2])

   r'''\new Voice {
      c'8 [ \glissando
      d'8 \glissando
      e'8 \glissando
      f'8 \glissando
      {
         g'8 \glissando
         a'8 ]
      }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [ \\glissando\n\td'8 \\glissando\n\te'8 \\glissando\n\tf'8 \\glissando\n\t{\n\t\tg'8 \\glissando\n\t\ta'8 ]\n\t}\n}"
