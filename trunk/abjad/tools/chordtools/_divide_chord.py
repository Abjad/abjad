from abjad.tools.chordtools.Chord import Chord
from abjad.components._Leaf import _Leaf
from abjad.tools import componenttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.chordtools.change_defective_chord_to_note_or_rest import change_defective_chord_to_note_or_rest
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


def _divide_chord(chord, pitch = NamedChromaticPitch('b', 3), attr = 'numbered_chromatic_pitch'):
   r'''Divide `chord` according to chromatic or diatonic pitch number of `pitch`.

   Return pair of newly created leaves.
   '''
   from abjad.tools import resttools
   from abjad.tools.notetools.Note import Note

   if not isinstance(chord, _Leaf):
      raise TypeError('%s is not a chord.' % str(chord))

   assert pitchtools.is_named_chromatic_pitch_token(pitch)
   assert attr in ('numbered_chromatic_pitch', 'numbered_diatonic_pitch')

   pitch = NamedChromaticPitch(pitch)
   treble = componenttools.clone_components_and_remove_all_spanners([chord])[0]
   bass = componenttools.clone_components_and_remove_all_spanners([chord])[0]

   markuptools.remove_markup_attached_to_component(treble)
   markuptools.remove_markup_attached_to_component(bass)
   
   if isinstance(treble, Note):
      if getattr(treble.pitch, attr) < getattr(pitch, attr):
         treble = resttools.Rest(treble)
   elif isinstance(treble, resttools.Rest):
      pass
   elif isinstance(treble, Chord):
      for note_head in treble.note_heads:
         if getattr(note_head.pitch, attr) < getattr(pitch, attr):
            treble.remove(note_head)
   else:
      raise ValueError('must be note, rest or chord.')

   if isinstance(bass, Note):
      if getattr(pitch, attr) <= getattr(bass.pitch, attr):
         bass = resttools.Rest(bass)
   elif isinstance(bass, resttools.Rest):
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
