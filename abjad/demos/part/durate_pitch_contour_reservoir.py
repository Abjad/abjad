import abjad


def durate_pitch_contour_reservoir(pitch_contour_reservoir):
    r'''Durates pitch contour reservoir.
    '''
    names = [
        'First Violin',
        'Second Violin',
        'Viola',
        'Cello',
        'Bass',
        ]
    durated_reservoir = {}
    for i, name in enumerate(names):
        long_duration = abjad.Duration(1, 2) * pow(2, i)
        short_duration = long_duration / 2
        rest_duration = long_duration * abjad.Multiplier(3, 2)
        div = rest_duration // abjad.Duration(3, 2)
        mod = rest_duration % abjad.Duration(3, 2)
        initial_rest = abjad.MultimeasureRest((3, 2)) * div
        maker = abjad.LeafMaker()
        if mod:
            initial_rest += maker([None], mod)
        durated_contours = [tuple(initial_rest)]
        pitch_contours = pitch_contour_reservoir[name]
        durations = [long_duration, short_duration]
        counter = 0
        maker = abjad.LeafMaker()
        for pitch_contour in pitch_contours:
            contour = []
            for pitch in pitch_contour:
                leaves = maker([pitch], [durations[counter]])
                contour.extend(leaves)
                counter = (counter + 1) % 2
            durated_contours.append(tuple(contour))
        durated_reservoir[name] = tuple(durated_contours)
    return durated_reservoir
