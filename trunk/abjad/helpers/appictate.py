from abjad.helpers.instances import instances


### TODO - write tests

def appictate(expr):
   '''
   Apply ascending chromatic pitches from zero to the notes and chords in expr.
   Used primarily in generating test and doc file examples. Coined term.
   '''

   for i, x in enumerate(instances(expr, '_Leaf')):
      if x.kind('Note'):
         x.pitch = i
      elif x.kind('Chord'):
         x.pitches = [i] 
      else:
         pass
