# -*- coding: utf-8 -*-
import random
from abjad.demos.mozart.make_mozart_measure_corpus \
    import make_mozart_measure_corpus


def choose_mozart_measures():
    r'''Chooses Mozart measures.
    '''

    measure_corpus = make_mozart_measure_corpus()
    chosen_measures = []
    for i, choices in enumerate(measure_corpus):
        if i == 7: # get both alternative endings for mm. 8
            chosen_measures.extend(choices)
        else:
            choice = random.choice(choices)
            chosen_measures.append(choice)
    return chosen_measures
