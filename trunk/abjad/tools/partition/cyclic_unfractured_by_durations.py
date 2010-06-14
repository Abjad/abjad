from abjad.tools.partition._by_durations import _by_durations


def cyclic_unfractured_by_durations(components, durations, tie_after = False):
   r'''Partition `components` cyclically by `durations`
   but do not fracture spanners in the process::

      abjad> staff = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> Beam(staff[0])
      abjad> Beam(staff[1])
      abjad> Slur(staff.leaves)
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'8 [ (
            d'8 ]
         }
         {
            \time 2/8
            e'8 [
            f'8 ] )
         }
      }
      
   ::
      
      abjad> durations = [Rational(3, 32)]
      abjad> partition.cyclic_unfractured_by_durations(staff.leaves, durations) 
      [[Note(c', 16.)], [Note(c', 32), Note(d', 16)], 
      [Note(d', 16), Note(e', 32)], [Note(e', 16.)], [Note(f', 16.)], [Note(f', 32)]]
      
   ::
      
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'16. [ (
            c'32
            d'16
            d'16 ]
         }
         {
            \time 2/8
            e'32 [
            e'16.
            f'16.
            f'32 ] )
         }
      }
   
   Return list of partitioned components.
   '''

   return _by_durations(components, durations, 
      spanners = 'unfractured', cyclic = True, tie_after = tie_after)
