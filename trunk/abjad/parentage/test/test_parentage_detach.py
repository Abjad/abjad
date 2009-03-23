from abjad import *
import py.test


def test_parentage_detach_01( ):
   '''Unspanned leaves can parentage-detach.'''

   t = Staff(scale(4))
   note = t[1]
   note.parentage._detach( )

   r'''
   \new Staff {
           c'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8\n\te'8\n\tf'8\n}"
   
   assert check(t)
   assert check(note)
   assert note.parentage.parent is None


def test_parentage_detach_02( ):
   '''Spanned leaves can parentage-detach.
      Spanners continue to attach to parentage-detached leaves.'''

   t = Staff([Voice(scale(4))])
   p = Beam(t.leaves)
   leaf = t.leaves[0]

   r'''
   \new Staff {
           \new Voice {
                   c'8 [
                   d'8
                   e'8
                   f'8 ]
           }
   }
   '''

   leaf.parentage._detach( )
   t.embed(0, leaf)

   r'''
   \new Staff {
           c'8 [
           \new Voice {
                   d'8
                   e'8
                   f'8 ]
           }
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8 [\n\t\\new Voice {\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"

   py.test.skip('TODO: Make work with new next and prev navigation.')

   assert check(t)
   assert check(leaf)


def test_parentage_detach_03( ):
   '''Unspanned containers can parent-detach.'''

   t = Staff(Sequential(run(2)) * 3)
   diatonicize(t)
   sequential = t[1]

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
   
   sequential.parentage._detach( )

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
   assert check(sequential)


def test_parentage_detach_04( ):
   '''Spanned containers parentage-detach successfully.
      Spanners continue to attach to parentage-detached containers.'''

   t = Staff([Voice(Sequential(run(2)) * 2)])
   sequential = t[0][0]
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

   sequential.parentage._detach( )
   t.embed(0, sequential)
   
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
   
   py.test.skip('TODO: Make work with new next and prev leaf navigation.')

   assert check(t)
