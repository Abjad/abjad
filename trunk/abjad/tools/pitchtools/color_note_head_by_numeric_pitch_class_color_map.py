from abjad.exceptions import MissingPitchError
from abjad.exceptions import ExtraPitchError
from abjad.tools import schemetools
from abjad.tools.pitchtools.get_named_pitch_from_pitch_carrier import get_named_pitch_from_pitch_carrier


def color_note_head_by_numeric_pitch_class_color_map(pitch_carrier):
   r'''Color `pitch_carrier` by pitch-class.

   ::

      abjad> t = Note(0, (1, 4))
      abjad> pitchtools.color_note_head_by_numeric_pitch_class_color_map(t)
      abjad> print t.format
      \once \override NoteHead #'color = #(x11-color 'red)
      c'4
   
   Pitch-class colors are these.

   * 0: red
   * 1: MediumBlue
   * 2: orange
   * 3: LightSlateBlue
   * 4: ForestGreen
   * 5: MediumOrchid
   * 6: firebrick
   * 7: DeepPink
   * 8: DarkOrange
   * 9: IndianRed
   * 10: CadetBlue
   * 11: SeaGreen
   * 12: LimeGreen

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.color_by_pc( )`` to
      ``pitchtools.color_note_head_by_numeric_pitch_class_color_map( )``.
   '''
   
   pitch = get_named_pitch_from_pitch_carrier(pitch_carrier)
   color = _pc_number_to_color(pitch.pc.number)
   if color is not None:
      pitch_carrier.note_head.color = color


def _pc_number_to_color(pc):
   
   pc_number_to_color = {
      0: schemetools.SchemeColor('red'),
      1: schemetools.SchemeColor('MediumBlue'),
      2: schemetools.SchemeColor('orange'),
      3: schemetools.SchemeColor('LightSlateBlue'),
      4: schemetools.SchemeColor('ForestGreen'),
      5: schemetools.SchemeColor('MediumOrchid'),
      6: schemetools.SchemeColor('firebrick'),
      7: schemetools.SchemeColor('DeepPink'),
      8: schemetools.SchemeColor('DarkOrange'),
      9: schemetools.SchemeColor('IndianRed'),
     10: schemetools.SchemeColor('CadetBlue'),
     11: schemetools.SchemeColor('SeaGreen'),
     12: schemetools.SchemeColor('LimeGreen')}

   return pc_number_to_color.get(pc, None)
