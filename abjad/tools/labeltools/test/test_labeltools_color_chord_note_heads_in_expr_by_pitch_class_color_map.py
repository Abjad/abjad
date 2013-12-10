# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_color_chord_note_heads_in_expr_by_pitch_class_color_map_01():

    chord = Chord([12, 14, 18, 21, 23], (1, 4))
    pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
    colors = ['red', 'blue', 'green']
    color_map = pitchtools.NumberedPitchClassColorMap(pitches, colors)
    labeltools.color_chord_note_heads_in_expr_by_pitch_class_color_map(
        chord, color_map)

    assert systemtools.TestManager.compare(
        chord,
        r'''
        <
            \tweak #'color #red
            c''
            \tweak #'color #red
            d''
            \tweak #'color #green
            fs''
            \tweak #'color #green
            a''
            \tweak #'color #blue
            b''
        >4
        '''
        )

    assert inspect(chord).is_well_formed()
