from abjad import *


def test_assess_components_strict_none_01( ):
   '''True for strictly contiguous leaves in voice.
      False for other time orderings of leaves in voice.'''

   t = Voice(scale(4))
   
   assert assess_components(t.leaves, contiguity = 'strict')

   assert not assess_components(list(reversed(t.leaves)), 
      contiguity = 'strict')
   assert not assess_components(t.leaves[2:] + t.leaves[:2], 
      contiguity = 'strict')
   assert not assess_components(t[3:4] + t[0:1], contiguity = 'strict')
   assert not assess_components([t] + t.leaves, contiguity = 'strict')


def test_assess_components_strict_none_02( ):
   '''True for strictly contiguous components.'''

   t = Voice(Container(run(2)) * 2)
   diatonicize(t)

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

   assert assess_components([t], contiguity = 'strict')
   assert assess_components(t[:], contiguity = 'strict')
   assert assess_components(t[0][:], contiguity = 'strict')
   assert assess_components(t[1][:], contiguity = 'strict')
   assert assess_components(t[0:1] + t[1][:], contiguity = 'strict')
   assert assess_components(t[0][:] + t[1:2], contiguity = 'strict')
   assert assess_components(t.leaves, contiguity = 'strict')


def test_assess_components_strict_none_03( ):
   '''Unicorporated leaves can not be evaluated for contiguity.'''

   t = scale(4)

   assert assess_components(t, contiguity = 'strict')
   assert not assess_components(t, contiguity = 'strict', 
      allow_orphans = False)


def test_assess_components_strict_none_04( ):
   '''Empty list returns True.'''

   t = [ ]

   assert assess_components(t, contiguity = 'strict')
