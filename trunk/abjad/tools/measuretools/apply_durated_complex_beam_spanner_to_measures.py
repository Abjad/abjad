from abjad.spanners import DuratedComplexBeam


def apply_durated_complex_beam_spanner_to_measures(measures):
   r'''.. versionadded:: 1.1.1
   
   Apply durated complex beam spanner to `measures`::

      abjad> staff = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'8
            d'8
         }
         {
            \time 2/8
            e'8
            f'8
         }
      }
      
   ::
      
      abjad> measures = staff[:]
      abjad> measuretools.apply_durated_complex_beam_spanner_to_measures(measures)
      DuratedComplexBeam(|2/8(2)|, |2/8(2)|)
      
   ::
      
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #1
            c'8 [
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #1
            d'8
         }
         {
            \time 2/8
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #1
            e'8
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #0
            f'8 ]
         }
      }

   Set beam spanner durations to preprolated measure durations.

   Return beam spanner created.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.beam_together( )``.
   '''

   durations = [ ]
   for measure in measures:
      measure.beam.unspan( )
      durations.append(measure.duration.preprolated)
   beam = DuratedComplexBeam(measures, durations = durations, span = 1)
   return beam
