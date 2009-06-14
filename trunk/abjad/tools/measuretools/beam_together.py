from abjad.beam import BeamComplexDurated


def beam_together(measures):
   '''Apply BeamComplexDurated to all measures in measures;
      set p.durations equal to preprolated measure durations.'''

   durations = [ ]
   for measure in measures:
      measure.beam.unspan( )
      durations.append(measure.duration.preprolated)
   beam = BeamComplexDurated(measures, durations = durations, span = 1)
   return beam
