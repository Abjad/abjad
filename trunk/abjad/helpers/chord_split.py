#from abjad.chord.chord import Chord
#from abjad.helpers.chord_cast_defective import chord_cast_defective
from abjad.helpers.engender import engender
from abjad.helpers.is_pitch_token import _is_pitch_token
from abjad.leaf.leaf import _Leaf
#from abjad.note.note import Note
from abjad.pitch.pitch import Pitch
#from abjad.rest.rest import Rest
#import operator


def _prune_notehead(part, notehead, pitch, attr, comparison):
   if attr == 'number':
      if comparison(notehead.pitch.number, pitch.number):
         part.remove(notehead)
   elif attr == 'altitude':
      if comparison(notehead.pitch.altitude, pitch.altitude):
         part.remove(notehead)
   else:
      raise ValueError('unknown pitch attr.')

def chord_split(chord, pitch = Pitch('b', 3), attr = 'number'):
   '''
   Return disjunct (treble, bass) pair of 'parts' from input chord;
   treble pitches greater than or equal to pitch attr;
   bass pitches all less than pitch attr.

   Input constraints:
      Input is canonically a (many-note) chord;
      input may also be a (one-note) note.

   Attr options:
      number
      altitude

   Length treatment:
      Zero-length parts return skip;
      length-one parts return note;
      Return parts of length greater than one return chord.

   ID treatment:
      Unique 'return part' IDs with input chord left unaltered.
      That is: id(chord) != id(treble) != (bass).
   
   Spanners treatment:
      Spanned source chords produce spanned output chords;
      natural by-product of the copy operation employed here.
   '''

   #assert isinstance(chord, (Note, Rest, Chord))
   #assert isinstance(pitch, Pitch)
   #assert attr in ('number', 'altitude')

#   if isinstance(chord, Chord):
#      treble, bass = chord.copy( ), chord.copy( )
#      for notehead in treble.noteheads:
#         _prune_notehead(treble, notehead, pitch, attr, operator.lt)
#      treble = chord_cast_defective(treble)
#      for notehead in bass.noteheads:
#         _prune_notehead(bass, notehead, pitch, attr, operator.ge)
#      bass = chord_cast_defective(bass)
#
#   elif isinstance(chord, Note):
#      note = chord
#      treble, bass = note.copy( ), note.copy( )
#      if attr == 'number':
#         if note.pitch.number >= pitch.number:
#            bass = Rest(bass)
#         else:
#            treble = Rest(treble)
#      elif attr == 'altitude':
#         if note.pitch.altitude >= pitch.altitude:
#            bass = Rest(bass)
#         else:
#            treble = Rest(treble)
#      else:
#         raise ValueError('unknown attr.')
#      print treble, bass
#
#   elif isinstance(chord, Rest):
#      treble = Rest(chord.duration.written.pair)
#      bass = Rest(chord.duration.written.pair)
#      
#   return treble, bass

   assert isinstance(chord, _Leaf)
   assert _is_pitch_token(pitch)
   assert attr in ('number', 'altitude')

   pitch = Pitch(pitch)
#   if isinstance(pitch, tuple):
#      pitch = Pitch(*pitch)
#   elif isinstance(pitch, (int, long, float)):
#      pitch = Pitch(pitch)

   treble = [ ]
   bass = [ ]
   for p in chord.pitches:
      if getattr(p, attr) < getattr(pitch, attr):
         bass.append(p.pair)   
      else:
         treble.append(p.pair)
   treble = engender(treble, chord.duration.written.pair)
   bass = engender(bass, chord.duration.written.pair)
   return treble, bass
   
