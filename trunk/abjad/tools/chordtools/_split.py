from abjad.components._Leaf import _Leaf
from abjad.components.Chord import Chord
from abjad.components.Note import Note
from abjad.components.Rest import Rest
from abjad.tools import componenttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.chordtools.change_defective_chord_to_note_or_rest import change_defective_chord_to_note_or_rest
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


def _split(chord, pitch = NamedChromaticPitch('b', 3), attr = 'numbered_chromatic_pitch'):
   r'''Split ``chord`` into a disjunt ``(treble, bass)`` pair
   of parts about ``pitch``. 
   Place pitches in ``chord`` greater than or equal to 
   ``pitch.attr`` into the treble part of the return pair. 
   Place pitches less than ``pitch.attr`` into the bass part 
   of the return pair.

   In the usual case, ``chord`` is an Abjad 
   :class:`~abjad.components.Chord.chord.Chord`. But ``input`` may also
   be an Abjad :class:`~abjad.components.Note.note.Note` or 
   :class:`~abjad.components.Rest.rest.Rest`.

   * ``attr``: ``chromatic_pitch_number``, ``numbered_diatonic_pitch``. 

   Length treatment:

   * Zero-length parts return as Abjad \
      :class:`~abjad.components.Rest.rest.Rest` instances.
   * Length-one parts return as Abjad \
      :class:`~abjad.components.Note.note.Note` instances.
   * Parts of length greater than ``1`` return as \
      :class:`~abjad.components.Chord.chord.Chord` instances.

   Note that both ``treble`` and ``bass`` return parts carry \
   unique IDs. That is::

      id(chord) != id(treble) != (bass)
   
   Note also that this function returns only unspanned output.

   Example::

      abjad> chord = Chord(range(12), Fraction(1, 4))
      abjad> chord
      Chord(c' cs' d' ef' e' f' fs' g' af' a' bf' b', 4)
      abjad> chordtools.split(chord, NamedChromaticPitch(6))
      (Chord(fs' g' af' a' bf' b', 4), Chord(c' cs' d' ef' e' f', 4))'''

   assert isinstance(chord, _Leaf)
   assert pitchtools.is_named_chromatic_pitch_token(pitch)
   assert attr in ('numbered_chromatic_pitch', 'numbered_diatonic_pitch')

   pitch = NamedChromaticPitch(pitch)
   treble = componenttools.clone_components_and_remove_all_spanners([chord])[0]
   bass = componenttools.clone_components_and_remove_all_spanners([chord])[0]

   #treble.markup.down[:] = [ ]
   #bass.markup.up[:] = [ ]
   markuptools.remove_markup_attached_to_component(treble)
   markuptools.remove_markup_attached_to_component(bass)
   
   if isinstance(treble, Note):
      if getattr(treble.pitch, attr) < getattr(pitch, attr):
         treble = Rest(treble)
   elif isinstance(treble, Rest):
      pass
   elif isinstance(treble, Chord):
      for note_head in treble.note_heads:
         if getattr(note_head.pitch, attr) < getattr(pitch, attr):
            treble.remove(note_head)
   else:
      raise ValueError('must be note, rest or chord.')

   if isinstance(bass, Note):
      if getattr(pitch, attr) <= getattr(bass.pitch, attr):
         bass = Rest(bass)
   elif isinstance(bass, Rest):
      pass
   elif isinstance(bass, Chord):
      for note_head in bass.note_heads:
         if getattr(pitch, attr) <= getattr(note_head.pitch, attr):
            bass.remove(note_head)
   else:
      raise ValueError('must be note, rest or chord.')

   treble = change_defective_chord_to_note_or_rest(treble)
   bass = change_defective_chord_to_note_or_rest(bass)

   return treble, bass
