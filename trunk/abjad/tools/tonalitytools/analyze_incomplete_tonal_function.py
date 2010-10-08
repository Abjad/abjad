from abjad.tools.tonalitytools.analyze_incomplete_chord import \
   analyze_incomplete_chord
from abjad.tools.tonalitytools.ChordClass import ChordClass
from abjad.tools.tonalitytools.Scale import Scale
from abjad.tools.tonalitytools.TonalFunction import TonalFunction


## TODO: Write tests ##
def analyze_incomplete_tonal_function(expr, key_signature):
   '''.. versionadded:: 1.1.2

   Analyze `expr` and return tonal function according to `key_signature`.
   '''

   if isinstance(expr, ChordClass):
      chord_class = expr
   else:
      chord_class = analyze_incomplete_chord(expr)
   root = chord_class.root
   scale = Scale(key_signature)
   scale_degree = scale.named_chromatic_pitch_class_to_scale_degree(root)
   quality = chord_class.quality_indicator.quality_string
   extent = chord_class.extent
   inversion = chord_class.inversion
   tonal_function = TonalFunction(scale_degree, quality, extent, inversion)

   return tonal_function
