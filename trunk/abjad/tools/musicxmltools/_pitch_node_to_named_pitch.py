from abjad.tools.musicxmltools._all_are_nodes_with_tag import _all_are_nodes_with_tag
from abjad.tools.pitchtools import Accidental
from abjad.tools.pitchtools import NamedChromaticPitch
from abjad.tools.pitchtools import apply_accidental_to_named_chromatic_pitch


def _pitch_node_to_named_pitch(node):
    assert _all_are_nodes_with_tag([node], 'note')
    step = node.find('step').text
    octave = int(node.find('octave').text)
    pitch = NamedChromaticPitch(step, octave)
    if node.find('alter') is not None:
        return apply_accidental_to_named_chromatic_pitch(
            pitch, Accidental(int(node.find('alter').text)))
    return pitch
