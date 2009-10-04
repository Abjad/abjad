from abjad import *


def test_check_assess_components_strict_parent_01( ):
   '''True for strictly contiguous leaves in voice.
      False for other time orderings of leaves in voice.'''

   t = Voice(construct.scale(4))
   
   assert check.assess_components(t.leaves, 
      contiguity = 'strict', share = 'parent')

   assert not check.assess_components(list(reversed(t.leaves)), 
      contiguity = 'strict', share = 'parent')

   components = [ ]
   components.extend(t.leaves[2:])
   components.extend(t.leaves[:2])
   assert not check.assess_components(components,
      contiguity = 'strict', share = 'parent')

   components = [ ]
   components.extend(t.leaves[3:4])
   components.extend(t.leaves[0:1])
   assert not check.assess_components(components,
      contiguity = 'strict', share = 'parent')

   components = [t]
   components.extend(t.leaves)
   assert not check.assess_components(components,
      contiguity = 'strict', share = 'parent')


def test_check_assess_components_strict_parent_02( ):
   '''True for unincorporated components when orphans allowed.
      False to unincorporated components when orphans not allowed.'''

   t = Voice(Container(construct.run(2)) * 2)
   pitchtools.diatonicize(t)

   r'''\new Voice {
           {
                   c'8
                   d'8
           }
           {
                   e'8
                   f'8
           }
   }'''

   assert check.assess_components([t], contiguity = 'strict', share = 'parent')
   assert not check.assess_components([t], allow_orphans = False, 
      contiguity = 'strict', share = 'parent')

   assert check.assess_components(t[:], contiguity = 'strict', share = 'parent')

   assert check.assess_components(t[0][:], contiguity = 'strict', share = 'parent')
   assert check.assess_components(t[1][:], contiguity = 'strict', share = 'parent')

   assert not check.assess_components(t.leaves, 
      contiguity = 'strict', share = 'parent')


def test_check_assess_components_strict_parent_03( ):
   '''True for orphan leaves when allow_orphans is True.
      False for orphan leaves when allow_orphans is False.'''

   t = construct.scale(4)

   assert check.assess_components(t, contiguity = 'strict', share = 'parent')
   assert not check.assess_components(t, allow_orphans = False, 
      contiguity = 'strict', share = 'parent')


def test_check_assess_components_strict_parent_04( ):
   '''Empty list returns True.'''

   t = [ ]

   assert check.assess_components(t, contiguity = 'strict', share = 'parent')
