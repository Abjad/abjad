from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch
from abjad.tools.pitchtools.pitch_number_to_octave_number import pitch_number_to_octave_number
from abjad.tools.pitchtools.pitch_class_number_to_pitch_name_with_sharps import pitch_class_number_to_pitch_name_with_sharps


def respell_named_pitches_in_expr_with_sharps(expr):
   r'''Renotate every pitch in `expr` with zero 
   or more sharps. ::

      abjad> staff = Staff(notetools.make_repeated_notes(6))
      abjad> pitchtools.set_ascending_chromatic_pitches_on_nontied_pitched_components_in_expr(staff)
      abjad> f(staff)
      \new Staff {
         c'8
         cs'8
         d'8
         ef'8
         e'8
         f'8
      }
      abjad> pitchtools.respell_named_pitches_in_expr_with_sharps(staff)
      abjad> f(staff)
      \new Staff {
         c'8
         cs'8
         d'8
         ds'8
         e'8
         f'8
      }

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.make_sharp( )`` to
      ``pitchtools.respell_named_pitches_in_expr_with_sharps( )``.
   '''
   from abjad.tools import leaftools

   if isinstance(expr, NamedPitch):
      _pitch_renotate_sharps(expr)
   else:
      for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
         if hasattr(leaf, 'pitches'):
            for pitch in leaf.pitches:
               _pitch_renotate_sharps(pitch)


def _pitch_renotate_sharps(pitch):
   octave = pitch_number_to_octave_number(pitch.number)
   name = pitch_class_number_to_pitch_name_with_sharps(pitch.pc)
   pitch.octave = octave
   pitch.name = name
