from abjad.beam.complex import BeamComplex


def beam_together(measures):
   '''Apply BeamComplex to all measures in measures;
      set p.durations equal to preprolated measure durations.'''

   durations = [ ]
   for measure in measures:
      measure.beam.unspan( )
      durations.append(measure.duration.preprolated)
   beam = BeamComplex(measures, durations = durations, span = 1)
   return beam
