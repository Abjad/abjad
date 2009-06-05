from abjad.leaf.leaf import _Leaf
from abjad.pitch.pitch import Pitch
from abjad.tools import construct
from abjad.tools import pitchtools


def split(chord, pitch = Pitch('b', 3), attr = 'number'):
   '''Split ``chord`` into a disjunt ``(treble, bass)`` pair
   of parts about ``pitch``. 
   Place pitches in ``chord`` greater than or equal to 
   ``pitch.attr`` into the treble part of the return pair. 
   Place pitches less than ``pitch.attr`` into the bass part 
   of the return pair.

   In the usual case, ``chord`` is an Abjad 
   :class:`~abjad.chord.chord.Chord`. But ``input`` may also
   be an Abjad :class:`~abjad.note.note.Note` or 
   :class:`~abjad.rest.rest.Rest`.

   * ``attr``: ``number``, ``alititude``. 

   Length treatment:

   * Zero-length parts return as Abjad \
      :class:`~abjad.rest.rest.Rest` instances.
   * Length-one parts return as Abjad \
      :class:`~abjad.note.note.Note` instances.
   * Parts of length greater than ``1`` return as \
      :class:`~abjad.chord.chord.Chord` instances.

   Note that both ``treble`` and ``bass`` return parts carry \
   unique IDs. That is::

      id(chord) != id(treble) != (bass)
   
   Note also that this function returns only unspanned output.

   Example::

      abjad> chord = Chord(range(12), Rational(1, 4))
      abjad> chord
      Chord(c' cs' d' ef' e' f' fs' g' af' a' bf' b', 4)
      abjad> chordtools.split(chord, Pitch(6))
      (Chord(fs' g' af' a' bf' b', 4), Chord(c' cs' d' ef' e' f', 4))'''

   assert isinstance(chord, _Leaf)
   assert pitchtools.is_token(pitch)
   assert attr in ('number', 'altitude')

   pitch = Pitch(pitch)
   treble = [ ]
   bass = [ ]

   for p in chord.pitches:
      if getattr(p, attr) < getattr(pitch, attr):
         bass.append(p.pair)   
      else:
         treble.append(p.pair)

   treble = construct.engender(treble, chord.duration.written)
   bass = construct.engender(bass, chord.duration.written)

   return treble, bass
