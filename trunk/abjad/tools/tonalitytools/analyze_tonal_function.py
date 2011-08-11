from abjad.tools.tonalitytools.ChordClass import ChordClass
from abjad.tools.tonalitytools.Scale import Scale
from abjad.tools.tonalitytools.TonalFunction import TonalFunction
from abjad.tools.tonalitytools.analyze_chord import analyze_chord


def analyze_tonal_function(expr, key_signature):
    '''.. versionadded:: 2.0

    Analyze `expr` and return tonal function according to `key_signature`. ::

        abjad> from abjad.tools import tonalitytools

    ::

        abjad> chord = Chord(['ef', 'g', 'bf'], (1, 4))
        abjad> key_signature = contexttools.KeySignatureMark('c', 'major')
        abjad> tonalitytools.analyze_tonal_function(chord, key_signature)
        FlatIIIMajorTriadInRootPosition

    Return none when no tonal function is understood. ::

        abjad> chord = Chord(['c', 'cs', 'd'], (1, 4))
        abjad> key_signature = contexttools.KeySignatureMark('c', 'major')
        abjad> tonalitytools.analyze_tonal_function(chord, key_signature) is None
        True

    Return tonal function or none.
    '''

    if isinstance(expr, ChordClass):
        chord_class = expr
    else:
        chord_class = analyze_chord(expr)

    if chord_class is None:
        return None

    root = chord_class.root
    scale = Scale(key_signature)
    scale_degree = scale.named_chromatic_pitch_class_to_scale_degree(root)
    quality = chord_class.quality_indicator.quality_string
    extent = chord_class.extent
    inversion = chord_class.inversion

    tonal_function = TonalFunction(scale_degree, quality, extent, inversion)
    return tonal_function
