# -*- coding: utf-8 -*-
import abjad
import copy


def add_bell_music_to_score(score):
    r'''Adds bell music to score.
    '''

    bell_voice = score['Bell Voice']

    def make_bell_phrase():
        phrase = []
        for _ in range(3):
            measure = abjad.Measure((6, 4), r"r2. a'2.")
            abjad.attach(abjad.LaissezVibrer(), measure[-1])
            phrase.append(measure)
            phrase.append(abjad.Measure((6, 4), 'R1.'))
        for _ in range(2):
            phrase.append(abjad.Measure((6, 4), 'R1.'))
        return phrase

    for _ in range(11):
        bell_voice.extend(make_bell_phrase())

    for _ in range(19):
        bell_voice.append(abjad.Measure((6, 4), 'R1.'))

    measure = abjad.Measure((6,4), r"a'1.")
    abjad.attach(abjad.LaissezVibrer(), measure[-1])
    bell_voice.append(measure)
