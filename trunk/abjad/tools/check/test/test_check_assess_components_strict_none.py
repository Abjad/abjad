from abjad import *


def test_check_assess_components_strict_none_01( ):
   '''True for strictly contiguous leaves in voice.
      False for other time orderings of leaves in voice.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   
   assert check.assess_components(t.leaves, contiguity = 'strict')

   components = list(reversed(t.leaves))
   assert not check.assess_components(components, contiguity = 'strict')

   components = [ ]
   components.extend(t.leaves[2:])
   components.extend(t.leaves[:2])
   assert not check.assess_components(components, contiguity = 'strict')

   components = [ ]
   components.extend(t.leaves[3:4])
   components.extend(t.leaves[0:1])
   assert not check.assess_components(components, contiguity = 'strict')

   components = [t]
   components.extend(t.leaves)
   assert not check.assess_components(components, contiguity = 'strict')


def test_check_assess_components_strict_none_02( ):
   '''True for strictly contiguous components.'''

   t = Voice(Container(leaftools.make_repeated_notes(2)) * 2)
   pitchtools.diatonicize(t)

   r'''
   \new Voice {
           {
                   c'8
                   d'8
           }
           {
                   e'8
                   f'8
           }
   }
   '''

   assert check.assess_components([t], contiguity = 'strict')
   assert check.assess_components(t[:], contiguity = 'strict')
   assert check.assess_components(t[0][:], contiguity = 'strict')
   assert check.assess_components(t[1][:], contiguity = 'strict')
   assert check.assess_components(t[0:1] + t[1][:], contiguity = 'strict')
   assert check.assess_components(t[0][:] + t[1:2], contiguity = 'strict')
   assert check.assess_components(t.leaves, contiguity = 'strict')


def test_check_assess_components_strict_none_03( ):
   '''Unicorporated leaves can not be evaluated for contiguity.'''

   t = leaftools.make_first_n_notes_in_ascending_diatonic_scale(4)

   assert check.assess_components(t, contiguity = 'strict')
   assert not check.assess_components(t, contiguity = 'strict', 
      allow_orphans = False)


def test_check_assess_components_strict_none_04( ):
   '''Empty list returns True.'''

   t = [ ]

   assert check.assess_components(t, contiguity = 'strict')
