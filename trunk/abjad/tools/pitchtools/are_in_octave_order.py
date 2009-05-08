## TODO: Extend pitchtools.are_in_octave_order( ) to work on Abjad pitches ## 

def are_in_octave_order(pcs, pitches):
   '''True if all pitch-classes in 'pcs' appear 
      in octave-relative order in 'pitches'.

      'pcs': list of pitch-classes.
      'pitches': list of pitches.

      abjad> pcs = [2, 7, 10]
      abjad> pitches = [6, 9, 12, 13, 14, 19, 22, 27, 28, 29, 32, 35]
      abjad> pitchtools.are_in_octave_order(pcs, pitches)
      True'''

   pcsStartIndex = [p % 12 for p in pitches].index(pcs[0] % 12)
   pcsTransposition = pitches[pcsStartIndex] - pcs[0]
   transposedPCs = [p + pcsTransposition for p in pcs]
   return set(transposedPCs).issubset(set(pitches))
