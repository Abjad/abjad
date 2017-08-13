import abjad


def make_mozart_measure(measure_dict):
    r'''Makes Mozart measure.
    '''
    # parse the contents of a measure definition dictionary
    # wrap the expression to be parsed inside a LilyPond { } block
    treble = abjad.parse('{{ {} }}'.format(measure_dict['t']))
    bass = abjad.parse('{{ {} }}'.format(measure_dict['b']))
    return treble, bass
