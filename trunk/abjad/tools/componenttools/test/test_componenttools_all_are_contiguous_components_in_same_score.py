from abjad import *


def test_componenttools_all_are_contiguous_components_in_same_score_01( ):
   '''True for strictly contiguous leaves in voice.
      False for other time orderings of leaves in voice.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   
   assert componenttools.all_are_contiguous_components_in_same_score(
      t.leaves)

   assert not componenttools.all_are_contiguous_components_in_same_score(list(reversed(t.leaves)), 
      )

   components = [ ]
   components.extend(t.leaves[2:])
   components.extend(t.leaves[:2])
   assert not componenttools.all_are_contiguous_components_in_same_score(components,
      )

   components = [ ]
   components.extend(t.leaves[3:4])
   components.extend(t.leaves[0:1])
   assert not componenttools.all_are_contiguous_components_in_same_score(components,
      )

   components = [t]
   components.extend(t.leaves)
   assert not componenttools.all_are_contiguous_components_in_same_score(components,
      )


def test_componenttools_all_are_contiguous_components_in_same_score_02( ):
   '''True for unincorporated components.
      True across container boundaries.'''

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

   assert componenttools.all_are_contiguous_components_in_same_score([t])
   assert componenttools.all_are_contiguous_components_in_same_score(t[:])
   assert componenttools.all_are_contiguous_components_in_same_score(
      t[0][:])
   assert componenttools.all_are_contiguous_components_in_same_score(
      t[1][:])
   assert componenttools.all_are_contiguous_components_in_same_score(
      t.leaves)


def test_componenttools_all_are_contiguous_components_in_same_score_03( ):
   '''True for orphan components when allow_orphans is True.
      False for orphan components when allow_orphans is False.'''

   t = leaftools.make_first_n_notes_in_ascending_diatonic_scale(4)

   assert componenttools.all_are_contiguous_components_in_same_score(t)
   assert not componenttools.all_are_contiguous_components_in_same_score(t, allow_orphans = False, 
      )


def test_componenttools_all_are_contiguous_components_in_same_score_04( ):
   '''Empty list returns True.'''

   t = [ ]

   assert componenttools.all_are_contiguous_components_in_same_score(t)
