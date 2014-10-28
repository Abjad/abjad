# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools import schemetools
from abjad.tools.topleveltools import override


def color_note_head_by_numbered_pitch_class_color_map(pitch_carrier):
    r'''Color `pitch_carrier` note head:

    ::

        >>> note = Note("c'4")

    ::

        >>> labeltools.color_note_head_by_numbered_pitch_class_color_map(note)
        Note("c'4")

    ..  doctest::

        >>> print(format(note))
        \once \override NoteHead #'color = #(x11-color 'red)
        c'4

    ::

        >>> show(note) # doctest: +SKIP

    Numbered pitch-class color map:

    ::

        0: red
        1: MediumBlue
        2: orange
        3: LightSlateBlue
        4: ForestGreen
        5: MediumOrchid
        6: firebrick
        7: DeepPink
        8: DarkOrange
        9: IndianRed
        10: CadetBlue
        11: SeaGreen
        12: LimeGreen

    Numbered pitch-class color map can not be changed.

    Raise type error when `pitch_carrier` is not a pitch carrier.

    Raise extra pitch error when `pitch_carrier` carries more than 1 note head.

    Raise missing pitch error when `pitch_carrier` carries no note head.

    Return `pitch_carrier`.
    '''

    pitch = pitchtools.NamedPitch.from_pitch_carrier(pitch_carrier)
    color = _pc_number_to_color(pitch.numbered_pitch_class.pitch_class_number)
    if color is not None:
        override(pitch_carrier).note_head.color = color
    return pitch_carrier


# TODO: externalize somewhere and make public
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