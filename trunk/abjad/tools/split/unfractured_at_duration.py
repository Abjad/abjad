from abjad.tools.split._at_duration import _at_duration


def unfractured_at_duration(component, prolated_duration, tie_after = False):
   r'''Split `component` at `prolated_duration`.
   Leave spanners untouched.
   Return split parts. ::

      abjad> t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
      abjad> pitchtools.diatonicize(t)
      abjad> Beam(t[0])
      abjad> Beam(t[1])
      abjad> Slur(t.leaves)
      abjad> f(t)
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

      abjad> halves = split.unfractured_at_duration(t.leaves[0], Rational(1, 32))
      abjad> f(t)
      \new Staff {
         {
            \time 2/8
            c'32 [ (
            c'16.
            d'8 ]
         }
         {
            \time 2/8
            e'8 [
            f'8 ] )
         }
      }

   Works on both leaves and containers.
   '''

   return _at_duration(component, prolated_duration, 
      spanners = 'unfractured', tie_after = tie_after)
