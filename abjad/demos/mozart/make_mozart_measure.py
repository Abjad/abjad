# -*- coding: utf-8 -*-
from abjad.tools.topleveltools import parse


def make_mozart_measure(measure_dict):
    r'''Makes Mozart measure.
    '''

    # parse the contents of a measure definition dictionary
    # wrap the expression to be parsed inside a LilyPond { } block
    treble = parse('{{ {} }}'.format(measure_dict['t']))
    bass = parse('{{ {} }}'.format(measure_dict['b']))
    return treble, bass