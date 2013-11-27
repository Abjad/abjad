# -*- encoding: utf-8 -*-
from abjad import *


def create_pitch_contour_reservoir():
    r'''Creates pitch contour reservoir.
    '''

    scale = tonalanalysistools.Scale('a', 'minor')
    pitch_ranges = {
        'First Violin': pitchtools.PitchRange(("c'", "a'''")),
        'Second Violin': pitchtools.PitchRange(('a', "a''")),
        'Viola': pitchtools.PitchRange(('e', "a'")),
        'Cello': pitchtools.PitchRange(('a,', 'a')),
        'Bass': pitchtools.PitchRange(('c', 'a')),
    }

    reservoir = {}
    for instrument_name, pitch_range in pitch_ranges.iteritems():
        pitch_set = scale.create_named_pitch_set_in_pitch_range(pitch_range)
        pitches = sorted(pitch_set, reverse=True)
        pitch_descents = []
        for i in xrange(len(pitches)):
            descent = tuple(pitches[:i + 1])
            pitch_descents.append(descent)
        reservoir[instrument_name] = tuple(pitch_descents)

    return reservoir
