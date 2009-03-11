from abjad import *


def test_parentage_detach_01( ):
   '''Unspanned leaves detach from parent containers.'''

   t = Staff(scale(4))
   note = t[1]
   note.parentage.detach( )

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
   '''Spanned leaves detach from parent containers.
      Spanners continue to attach to detached leaves.'''

   t = Staff([Voice(scale(4))])
   p = Beam(t.leaves)

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

   #note, parent, index = t.leaves[0].parentage.detach( )
   #t.embed(index, note)
   receipt = t.leaves[0].parentage.detach( )
   t.embed(receipt.index, receipt.component)

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

   assert check(t)
   #assert check(note)
   assert check(receipt.component)


def test_parentage_detach_03( ):
   '''Unspanned containers detach from parent containers successfully.'''

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
   
   #sequential, parent, index = t[1].parentage.detach( )
   receipt = t[1].parentage.detach( )

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
   #assert check(sequential)
   assert check(receipt.component)


def test_parentage_detach_04( ):
   '''Spanned containers detach from parent containers successfully.
      Spanners continue to attach to detached containers.'''

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

   #sequential, parent, index = t[0][0].parentage.detach( )
   #t.embed(index, sequential)
   receipt = t[0][0].parentage.detach( )
   t.embed(receipt.index, receipt.component)
   
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
