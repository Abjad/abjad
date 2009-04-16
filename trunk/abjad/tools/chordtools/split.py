from abjad.leaf.leaf import _Leaf
from abjad.pitch.pitch import Pitch
from abjad.tools import construct
from abjad.tools import pitchtools


def split(chord, pch = Pitch('b', 3), attr = 'number'):
   '''Return disjunct (treble, bass) pair of 'parts' from input chord;
      treble pitches greater than or equal to pitch attr;
      bass pitches all less than pitch attr.

      Input constraints:
         * Input is canonically a (many-note) chord;
         * Input may also be a (one-note) note;
         * Input may also be a (no-note) rest.

      Attr options:
         `number`
         `altitude`

      Length treatment:
         * Zero-length parts engender rest;
         * length-one parts engender note;
         * Return parts of length greater than one engender chord.

      ID treatment:
         * Unique 'return part' IDs with input chord left unaltered.
         * That is: id(chord) != id(treble) != (bass).
      
      Spanners  treatment:
         * Helper engenders only unspanned output.'''

   assert isinstance(chord, _Leaf)
   assert pitchtools.is_token(pch)
   assert attr in ('number', 'altitude')

   pch = Pitch(pch)
   treble = [ ]
   bass = [ ]

   for p in chord.pitches:
      if getattr(p, attr) < getattr(pch, attr):
         bass.append(p.pair)   
      else:
         treble.append(p.pair)

   treble = construct.engender(treble, chord.duration.written)
   bass = construct.engender(bass, chord.duration.written)

   return treble, bass
