def pitch_renotate_sharps(pitch):
   octave = pitch.tools.pitchNumberToOctave(pitch.number)
   name = pitch.tools.pcToPitchNameSharps[pitch.pc]
   pitch.octave = octave
   pitch.name = name
