from abjad.clef.clef import Clef
from abjad.staff.staff import Staff
from abjad.staffgroup.pianostaff import PianoStaff


## this module houses all score 'skeleton' templates. ##

def piano( ):
   '''Standard piano template. 
      A PianoStaff named 'PianoStaff, and two staves inside of it each named
      'PianoBass' and 'PianoTreble'. 
      Bass clef is also added to the bass staff.'''

   ps = PianoStaff([ ])
   ps.name = 'PianoStaff'
   bass = Staff([ ])
   bass.name = 'PianoBass'
   bass.clef.forced = Clef('bass')
   treble = Staff([ ])
   treble.name = 'PianoTreble'
   ps.append(treble)
   ps.append(bass)
   return ps
