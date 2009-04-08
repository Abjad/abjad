from abjad import *
import py.test


def test_parentage_cut_01( ):
   '''Unspanned leaves can parentage-cut.'''

   t = Staff(scale(4))
   note = t[1]
   note.parentage._cut( )

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


def test_parentage_cut_02( ):
   '''Spanned leaves can parentage-cut.
      Spanners continue to attach to parentage-cut leaves.'''

   t = Voice([Container(scale(4))])
   p = Beam(t.leaves)
   leaf = t.leaves[0]

   r'''\new Voice {
      {
         c'8 [
         d'8
         e'8
         f'8 ]
      }
   }'''

   leaf.parentage._cut( )
   assert not check(t)
   assert not check(leaf)

   t._music.insert(0, leaf)
   leaf.parentage._switchParentTo(t)

   r'''\new Voice {
           c'8 [
           {
                   d'8
                   e'8
                   f'8 ]
           }
   }'''

   assert check(t)
   assert check(leaf)
   assert t.format == "\\new Voice {\n\tc'8 [\n\t{\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_parentage_cut_03( ):
   '''Unspanned containers can parent-cut.'''

   t = Staff(Container(run(2)) * 3)
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
   
   sequential.parentage._cut( )

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


def test_parentage_cut_04( ):
   '''Spanned containers parentage-cut successfully.
      Spanners continue to attach to parentage-cut containers.'''

   t = Voice([Container(FixedDurationTuplet((2, 8), scale(3)) * 2)])
   tuplet = t[0][0]
   p = Beam(t[0][:])

   r'''\new Voice {
      {
         \times 2/3 {
            c'8 [
            d'8
            e'8
         }
         \times 2/3 {
            c'8
            d'8
            e'8 ]
         }
      }
   }'''

   tuplet.parentage._cut( )
   assert not check(t)
   assert not check(tuplet)

   t._music.insert(0, tuplet)
   tuplet.parentage._switchParentTo(t)
   
   r'''\new Voice {
      \times 2/3 {
         c'8 [
         d'8
         e'8
      }
      {
         \times 2/3 {
            c'8
            d'8
            e'8 ]
         }
      }
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t{\n\t\t\\times 2/3 {\n\t\t\tc'8\n\t\t\td'8\n\t\t\te'8 ]\n\t\t}\n\t}\n}"
