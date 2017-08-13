import abjad


def make_desordre_measure(pitches):
    '''Makes a measure composed of *Désordre cells*.

    `pitches` is a list of lists of number (e.g., [[1, 2, 3], [2, 3, 4]])

    Returns a measure.
    '''
    for sequence in pitches:
        container = abjad.demos.ligeti.make_desordre_cell(sequence)
        time_signature = abjad.inspect(container).get_duration()
        time_signature = abjad.NonreducedFraction(time_signature)
        time_signature = time_signature.with_denominator(8)
        measure = abjad.Measure(time_signature, [container])
    return measure
