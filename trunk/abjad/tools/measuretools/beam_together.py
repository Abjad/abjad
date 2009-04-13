from abjad.beam.complex import ComplexBeam


def beam_together(measures):
   '''Apply ComplexBeam to all measures in measures;
      set p.durations equal to preprolated measure durations.'''

   durations = [ ]
   for measure in measures:
      measure.beam.unspan( )
      durations.append(measure.duration.preprolated)
   beam = ComplexBeam(measures, durations = durations, span = 1)
   return beam
