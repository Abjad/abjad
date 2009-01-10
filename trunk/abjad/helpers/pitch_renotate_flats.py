def pitch_renotate_flats(pitch):
   octave = pitch.tools.pitchNumberToOctave(pitch.number)
   name = pitch.tools.pcToPitchNameFlats[pitch.pc]
   pitch.octave = octave
   pitch.name = name
