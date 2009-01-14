from abjad import *


def test_container_detach_01( ):
   '''
   Unspanned containers detach from parent containers successfully.
   '''

   t = Staff(Sequential(run(2)) * 3)
   diatonicize(t)

   r'''
   \new Staff {
           {
                   c'8
                   d'8
           }
           {
                   e'8
                   f'8
           }
           {
                   g'8
                   a'8
           }
   }
   '''
   
   result = t[1].detach( )

   r'''
   \new Staff {
           {
                   c'8
                   d'8
           }
           {
                   g'8
                   a'8
           }
   }
   '''

   assert t.format == "\\new Staff {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
   assert check(t)
   assert check(result)


def test_container_detach_02( ):
   '''
   Spanned containers detach from parent containers successfully.
   Spanners continue to attach to detached containers.
   '''

   t = Staff([Voice(Sequential(run(2)) * 2)])
   p = Beam(t[0][ : ])

   r'''
   \new Staff {
           \new Voice {
                   {
                           c'8 [
                           c'8
                   }
                   {
                           c'8
                           c'8 ]
                   }
           }
   }
   '''

   t.embed(0, t[0][0].detach( ))
   
   r'''
   \new Staff {
           {
                   c'8 [
                   c'8
           }
           \new Voice {
                   {
                           c'8
                           c'8 ]
                   }
           }
   }
   '''

   assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t}\n\t\\new Voice {\n\t\t{\n\t\t\tc'8\n\t\t\tc'8 ]\n\t\t}\n\t}\n}"
   
   assert check(t)
