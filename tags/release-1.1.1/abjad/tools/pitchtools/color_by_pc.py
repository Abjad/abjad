from abjad.exceptions import MissingPitchError
from abjad.exceptions import ExtraPitchError
from abjad.scm import Color
from abjad.tools.pitchtools.get_pitch import get_pitch as \
   pitchtools_get_pitch


def color_by_pc(pitch_carrier):
   r'''Color *pitch_carrier* according to pitch-class.

   ::

      abjad> t = Note(0, (1, 4))
      abjad> pitchtools.color_by_pc(t)
      abjad> print t.format
      \once \override NoteHead #'color = #(x11-color 'red)
      c'4
   '''
   
   pitch = pitchtools_get_pitch(pitch_carrier)
   color = _pc_to_color(pitch.pc)
   if color is not None:
      pitch_carrier.notehead.color = color


def _pc_to_color(pc):
   
   pc_to_color = {
      0: Color('red'),
      1: Color('MediumBlue'),
      2: Color('orange'),
      3: Color('LightSlateBlue'),
      4: Color('ForestGreen'),
      5: Color('MediumOrchid'),
      6: Color('firebrick'),
      7: Color('DeepPink'),
      8: Color('DarkOrange'),
      9: Color('IndianRed'),
     10: Color('CadetBlue'),
     11: Color('SeaGreen'),
     12: Color('LimeGreen')}

   return pc_to_color.get(pc, None)
