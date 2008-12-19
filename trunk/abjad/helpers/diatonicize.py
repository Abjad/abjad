from abjad.helpers.instances import instances


### TODO - write tests

def diatonicize(expr):
   '''
   Apply ascending diatonic pitches from zero to the notes and chords in expr.
   Used primarily in generating test and doc file examples. 
   Compare with appicate( ) helper.
   '''

   diatonic_residues = (0, 2, 4, 5, 7, 9, 11)
   length = len(diatonic_residues)
   for i, x in enumerate(instances(expr, '_Leaf')):
      pitch = int(i / length) * 12 + diatonic_residues[i % length] 
      if x.kind('Note'):
         x.pitch = pitch
      elif x.kind('Chord'):
         x.pitches = [pitch] 
      else:
         pass
