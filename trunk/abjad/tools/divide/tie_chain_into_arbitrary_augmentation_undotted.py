from abjad.tools.divide._tie_chain_arbitrarily import _tie_chain_arbitrarily


def tie_chain_into_arbitrary_augmentation_undotted(tie_chain, divisions):
   r'''.. versionadded:: 1.1.2

   Divide `tie_chain` into fixed-duration tuplet according to 
   arbitrary integer `divisions`.

   Interpret `divisions` as a ratio. That is, reduce integers
   in `divisions` relative to each other.

   Return non-trivial tuplet as augmentation.

   Where ``divisions[i] == 1`` for ``i < len(divisions)``, 
   do not allow tupletted notes to carry dots. ::

      abjad> staff = Staff([Note(0, (1, 8)), Note(0, (1, 16)), Note(0, (1, 16))])
      abjad> Tie(staff[:2])
      Tie(c'8, c'16)
      abjad> Beam(staff[:])
      Beam(c'8, c'16, c'16)
      abjad> divide.tie_chain_into_arbitrary_augmentation_undotted(staff[0].tie.chain, [1])
      FixedDurationTuplet(3/16, [c'8])
      abjad> f(t)
      \new Staff {
              \fraction \times 3/2 {
                      c'8 [
              }
              c'16 ]
      }

   ::

      abjad> staff = Staff([Note(0, (1, 8)), Note(0, (1, 16)), Note(0, (1, 16))])
      abjad> Tie(staff[:2])
      Tie(c'8, c'16)
      abjad> Beam(staff[:])
      Beam(c'8, c'16, c'16)
      abjad> divide.tie_chain_into_arbitrary_augmentation_undotted(staff[0].tie.chain, [1, 2])
      FixedDurationTuplet(3/16, [c'16, c'8])
      abjad> f(staff)
      \new Staff {
              {
                      c'16 [
                      c'8
              }
              c'16 ]
      }

   ::

      abjad> staff = Staff([Note(0, (1, 8)), Note(0, (1, 16)), Note(0, (1, 16))])
      abjad> Tie(staff[:2])
      Tie(c'8, c'16)
      abjad> Beam(staff[:])
      Beam(c'8, c'16, c'16)
      abjad> divide.tie_chain_into_arbitrary_augmentation_undotted(staff[0].tie.chain, [1, 2, 2])
      FixedDurationTuplet(3/16, [c'32, c'16, c'16])
      abjad> f(staff)
      \new Staff {
              \fraction \times 6/5 {
                      c'32 [
                      c'16
                      c'16
              }
              c'16 ]
      }
   '''

   prolation, dotted = 'augmentation', False
   return _tie_chain_arbitrarily(tie_chain, divisions, prolation, dotted)
