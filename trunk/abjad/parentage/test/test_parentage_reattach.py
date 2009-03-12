from abjad import *


def test_parentage_reattach_01( ):
   '''Unspanned leaves can detach from parentage.
      Unspanned, detached leaves are well formed.
      Unspanned, detached leaves can reattach to parentage.
      Unspanned, reattached leaves are well formed.'''

   t = Staff(scale(4))
   note = t[1]
   receipt = note.parentage._detach( )

   r'''
   \new Staff {
           c'8
           e'8
           f'8
   }
   '''

   note.parentage._reattach(receipt)

   r'''
   \new Staff {
           c'8
           d'8
           e'8
           f'8
   }
   '''
   
   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_parentage_reattach_02( ):
   '''Spanned leaves can detach from parentage.
      Spanned, detached leaves are not well formed.
      Spanned, detached leaves can reattach to parentage.
      Spanned, reattached leaves are once again well formed.'''

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

   receipt = leaf.parentage._detach( )

   r'''
   \new Staff {
           \new Voice {
                   d'8
                   e'8
                   f'8 ]
           }
   }
   '''

   assert not check(t)

   leaf.parentage._reattach(receipt)

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

   assert check(t)
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_parentage_reattach_03( ):
   '''Unspanned containers can detach from parentage.
      Unspanned containers that detach are still well formed.
      Unspanned containers can reattach to parentage.
      Unspanend containers that reattach are still well formed.'''

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
   
   receipt = sequential.parentage._detach( )

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

   assert check(t)
   assert check(sequential)

   sequential.parentage._reattach(receipt)

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

   assert check(t)
   assert check(sequential)
   assert t.format == "\\new Staff {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
   

def test_parentage_reattach_04( ):
   '''Spanned containers can detach from parentage.
      Spanned containers detached from parentage are not well formed.
      Spanned containers can reattach to parentage.
      Spanned containers that reattach to parentage are again well formed.'''

   t = Staff([Voice(Sequential(run(2)) * 2)])
   sequential = t[0][0]
   diatonicize(t)
   p = Beam(t[0][ : ])

   r'''
   \new Staff {
           \new Voice {
                   {
                           c'8 [
                           d'8
                   }
                   {
                           e'8
                           f'8 ]
                   }
           }
   }
   '''

   receipt = sequential.parentage._detach( )

   r'''
   \new Staff {
           \new Voice {
                   {
                           e'8
                           f'8 ]
                   }
           }
   }
   '''

   assert not check(t)
   assert not check(sequential)

   sequential.parentage._reattach(receipt)

   r'''
   \new Staff {
           \new Voice {
                   {
                           c'8 [
                           d'8
                   }
                   {
                           e'8
                           f'8 ]
                   }
           }
   }
   '''

   assert check(t)
   assert check(sequential)
