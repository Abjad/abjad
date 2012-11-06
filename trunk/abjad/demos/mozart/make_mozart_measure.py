from abjad import *


def make_mozart_measure(measure_dict):
    # parse the contents of a measure definition dictionary
    # wrap the expression to be parsed inside a LilyPond { } block
    treble = p('{{ {} }}'.format(measure_dict['t']))
    bass = p('{{ {} }}'.format(measure_dict['b']))
    return treble, bass
