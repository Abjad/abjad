from abjad.components.Chord import Chord
from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch
from abjad.tools.pitchtools.pitch_number_to_octave_number import pitch_number_to_octave_number
from abjad.tools.pitchtools.pitch_class_number_to_pitch_name_with_flats import pitch_class_number_to_pitch_name_with_flats


def respell_named_pitches_in_expr_with_flats(expr):
   r'''Renotate every pitch in `expr` with zero or more flats.

   ::

      abjad> staff = Staff(notetools.make_repeated_notes(6))
      abjad> macros.chromaticize(staff)
      abjad> f(staff)
      \new Staff {
         c'8
         cs'8
         d'8
         ef'8
         e'8
         f'8
      }
      abjad> pitchtools.respell_named_pitches_in_expr_with_flats(staff)
      abjad> f(staff)
      \new Staff {
         c'8
         df'8
         d'8
         ef'8
         e'8
         f'8
      }

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.make_flat( )`` to
      ``pitchtools.respell_named_pitches_in_expr_with_flats( )``.
   '''
   from abjad.tools import leaftools


   if isinstance(expr, NamedPitch):
      #_pitch_renotate_flats(expr)
      return _new_pitch_with_flats(expr)
   else:
      for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
         #if hasattr(leaf, 'pitches'):
         #   for pitch in leaf.pitches:
         #      _pitch_renotate_flats(pitch)
         if isinstance(leaf, Chord):
            for note_head in leaf.note_heads:
               note_head.pitch = _new_pitch_with_flats(note_head.pitch)
         elif hasattr(leaf, 'pitch'):
            leaf.pitch = _new_pitch_with_flats(leaf.pitch)           


#def _pitch_renotate_flats(pitch):
#   octave = pitch_number_to_octave_number(pitch.pitch_number)
#   name = pitch_class_number_to_pitch_name_with_flats(pitch.pitch_class)
#   pitch.octave = octave
#   pitch.name = name


def _new_pitch_with_flats(pitch):
   octave = pitch_number_to_octave_number(pitch.pitch_number)
   name = pitch_class_number_to_pitch_name_with_flats(pitch.pitch_class)
   pitch = type(pitch)(name, octave)
   return pitch
