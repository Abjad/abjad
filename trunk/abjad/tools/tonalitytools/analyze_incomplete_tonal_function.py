from abjad.tools.tonalitytools.ChordClass import ChordClass
from abjad.tools.tonalitytools.Scale import Scale
from abjad.tools.tonalitytools.TonalFunction import TonalFunction
from abjad.tools.tonalitytools.analyze_incomplete_chord import analyze_incomplete_chord


# TODO: Write tests #
def analyze_incomplete_tonal_function(expr, key_signature):
    '''.. versionadded:: 2.0

    Analyze tonal function of `expr` according to `key_signature`::

        abjad> from abjad.tools import tonalitytools

    ::

        abjad> chord = Chord("<c' e'>4")
        abjad> key_signature = contexttools.KeySignatureMark('g', 'major')
        abjad> tonalitytools.analyze_incomplete_tonal_function(chord, key_signature)
        IVMajorTriadInRootPosition

    Return tonal function.
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
