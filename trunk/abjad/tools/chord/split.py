from abjad.helpers.engender import engender
from abjad.helpers.is_pitch_token import is_pitch_token
from abjad.leaf.leaf import _Leaf
from abjad.pitch.pitch import Pitch


def split(chord, pitch = Pitch('b', 3), attr = 'number'):
   '''Return disjunct (treble, bass) pair of 'parts' from input chord;
      treble pitches greater than or equal to pitch attr;
      bass pitches all less than pitch attr.

      Input constraints:
         Input is canonically a (many-note) chord;
         input may also be a (one-note) note;
         input may also be a (no-note) rest.

      Attr options:
         'number'
         'altitude'

      Length treatment:
         Zero-length parts engender rest;
         length-one parts engender note;
         Return parts of length greater than one engender chord.

      ID treatment:
         Unique 'return part' IDs with input chord left unaltered.
         That is: id(chord) != id(treble) != (bass).
      
      Spanners treatment:
         Helper engenders only unspanned output.'''

   assert isinstance(chord, _Leaf)
   assert is_pitch_token(pitch)
   assert attr in ('number', 'altitude')

   pitch = Pitch(pitch)
   treble = [ ]
   bass = [ ]

   for p in chord.pitches:
      if getattr(p, attr) < getattr(pitch, attr):
         bass.append(p.pair)   
      else:
         treble.append(p.pair)

   treble = engender(treble, chord.duration.written)
   bass = engender(bass, chord.duration.written)

   return treble, bass
