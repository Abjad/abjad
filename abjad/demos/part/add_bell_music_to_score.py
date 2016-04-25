# -*- coding: utf-8 -*-
import copy
from abjad.tools import indicatortools
from abjad.tools import scoretools


def add_bell_music_to_score(score):
    r'''Adds bell music to score.
    '''

    bell_voice = score['Bell Voice']

    def make_bell_phrase():
        phrase = []
        for _ in range(3):
            phrase.append(scoretools.Measure((6, 4), r"r2. a'2. \laissezVibrer"))
            phrase.append(scoretools.Measure((6, 4), 'R1.'))
        for _ in range(2):
            phrase.append(scoretools.Measure((6, 4), 'R1.'))
        return phrase

    for _ in range(11):
        bell_voice.extend(make_bell_phrase())

    for _ in range(19):
        bell_voice.append(scoretools.Measure((6, 4), 'R1.'))

    bell_voice.append(scoretools.Measure((6,4), r"a'1. \laissezVibrer"))
