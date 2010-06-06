from abjad.tools.pitchtools.get_pitches import get_pitches


def sort_by_pc(pitch_carriers):
   '''.. versionadded:: 1.1.2
   
   Return a newly created list of the the elements in `pitch_carriers`
   sorted in ascending order by pitch-class. ::

      abjad> chord = Chord([9, 11, 12, 14, 16], (1, 4))
      abjad> notes = chordtools.arpeggiate(chord)
      abjad> pitchtools.sort_by_pc(notes)      
      [Note(c'', 4), Note(d'', 4), Note(e'', 4), Note(a', 4), Note(b', 4)]

   Note that the elements in `pitch_carriers` are
   not changed in any way.
   '''

   result = list(pitch_carriers[:])
   result.sort(lambda x, y: cmp(
         get_pitches(x)[0].pc.number, 
         get_pitches(y)[0].pc.number))

   return result
