from abjad.tools.tonalharmony.analyze_chord import analyze_chord
from abjad.tools.tonalharmony.Scale import Scale
from abjad.tools.tonalharmony.TonalFunction import TonalFunction


def analyze_tonal_function(expr, key_signature):
   '''.. versionadded:: 1.1.2

   Analyze `expr` and return tonal function according to `key_signature`. ::

      abjad> chord = Chord(['ef', 'g', 'bf'], (1, 4))
      abjad> key_signature = KeySignature('c', 'major')
      abjad> tonalharmony.analyze_tonal_function(chord, key_signature)
      FlatIIIMajorTriadInRootPosition
   '''

   chord_class = analyze_chord(expr)
   root = chord_class.root
   scale = Scale(key_signature)
   scale_degree = scale.named_pitch_class_to_scale_degree(root)
   quality = chord_class.quality_indicator.quality_string
   extent = chord_class.extent
   inversion = chord_class.inversion
   tonal_function = TonalFunction(scale_degree, quality, extent, inversion)

   return tonal_function
