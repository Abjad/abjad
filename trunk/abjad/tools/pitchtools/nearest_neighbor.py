def nearest_neighbor(pitch_number, pc):
   '''Return integer pitch number within one tritone
   of `pitch_number` and with pitch class 
   equal to `pc`. ::

      abjad> pitchtools.nearest_neighbor(12, 0)
      12
      abjad> pitchtools.nearest_neighbor(12, 1)
      13
      abjad> pitchtools.nearest_neighbor(12, 2)
      14
      abjad> pitchtools.nearest_neighbor(12, 3)
      15
      abjad> pitchtools.nearest_neighbor(12, 4)
      16
      abjad> pitchtools.nearest_neighbor(12, 5)
      17
      abjad> pitchtools.nearest_neighbor(12, 6)
      6
      abjad> pitchtools.nearest_neighbor(12, 7)
      7
      abjad> pitchtools.nearest_neighbor(12, 8)
      8
      abjad> pitchtools.nearest_neighbor(12, 9)
      9
      abjad> pitchtools.nearest_neighbor(12, 10)
      10
      abjad> pitchtools.nearest_neighbor(12, 11)
      11
      abjad> pitchtools.nearest_neighbor(12, 12)
      12
   '''
   
   targetPC = pitch_number % 12
   down = (targetPC - pc) % 12
   up = (pc - targetPC) % 12
   if up < down:
      return pitch_number + up
   else:
      return pitch_number - down
