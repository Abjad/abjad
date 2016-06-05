# -*- coding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools import tonalanalysistools


def create_pitch_contour_reservoir():
    r'''Creates pitch contour reservoir.
    '''

    scale = tonalanalysistools.Scale('a', 'minor')
    pitch_ranges = {
        'First Violin': pitchtools.PitchRange('[C4, A6]'),
        'Second Violin': pitchtools.PitchRange('[A3, A5]'),
        'Viola': pitchtools.PitchRange('[E3, A4]'),
        'Cello': pitchtools.PitchRange('[A2, A3]'),
        'Bass': pitchtools.PitchRange('[C3, A3]'),
    }

    reservoir = {}
    for instrument_name, pitch_range in pitch_ranges.items():
        pitch_set = scale.create_named_pitch_set_in_pitch_range(pitch_range)
        pitches = sorted(pitch_set, reverse=True)
        pitch_descents = []
        for i in range(len(pitches)):
            descent = tuple(pitches[:i + 1])
            pitch_descents.append(descent)
        reservoir[instrument_name] = tuple(pitch_descents)

    return reservoir