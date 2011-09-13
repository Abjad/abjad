def _validate_pitch_classes(pitch_classes):
    numbers = [abs(pc) for pc in pitch_classes]
    numbers.sort()
    if not numbers == range(12):
        raise ValueError('must contain all twelve pitch-classes.')
