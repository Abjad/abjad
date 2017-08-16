import abjad


def create_pitch_contour_reservoir():
    r'''Creates pitch contour reservoir.
    '''

    scale = abjad.tonalanalysistools.Scale(('a', 'minor'))
    pitch_ranges = {
        'First Violin': abjad.PitchRange('[C4, A6]'),
        'Second Violin': abjad.PitchRange('[A3, A5]'),
        'Viola': abjad.PitchRange('[E3, A4]'),
        'Cello': abjad.PitchRange('[A2, A3]'),
        'Bass': abjad.PitchRange('[C3, A3]'),
    }

    reservoir = {}
    for name, pitch_range in pitch_ranges.items():
        pitch_set = scale.create_named_pitch_set_in_pitch_range(pitch_range)
        pitches = sorted(pitch_set, reverse=True)
        pitch_descents = []
        for i in range(len(pitches)):
            descent = tuple(pitches[:i + 1])
            pitch_descents.append(descent)
        reservoir[name] = tuple(pitch_descents)

    return reservoir
