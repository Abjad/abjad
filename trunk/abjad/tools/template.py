from abjad import *

### this module houses all score 'skeleton' templates.

def piano( ):
   '''
   Standard piano template. 
   A PianoStaff named 'PianoStaff, and two staves inside of it each named
   'PianoBass' and 'PianoTreble'. 
   Bass clef is also added to the bass staff.
   '''
   ps = PianoStaff([ ])
   ps.invocation.name = 'PianoStaff'
   bass = Staff([ ])
   bass.invocation.name = 'PianoBass'
   bass.clef = 'bass'
   treble = Staff([ ])
   treble.invocation.name = 'PianoTreble'
   ps.append(treble)
   ps.append(bass)
   return ps

