def set_artificial_harmonic(self, diatonicInterval = 'perfect fourth'):
   '''
   >>> l = note.Note(5, (1, 4))
   >>> l.setArtificialHarmonic('perfect fourth') 
   >>> l
   <f' bf'\\harmonic>4
   '''

   ### TODO - port forward ###

   self.harmonic = True
   capotasto = self.pitch.__class__(self.safePitchNumber)
   armonica = capotasto.diatonicTranspose(diatonicInterval)
   self.pitch = [capotasto, armonica]
