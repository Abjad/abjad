import copy
from abjad.tools import marktools
from abjad.tools import measuretools


def add_bell_music_to_score(score):

    bell_voice = score['Bell Voice']

    def make_bell_phrase():
        phrase = []
        for _ in range(3):
            phrase.append(measuretools.Measure((6, 4), r"r2. a'2. \laissezVibrer"))
            phrase.append(measuretools.Measure((6, 4), 'R1.'))
        for _ in range(2):
            phrase.append(measuretools.Measure((6, 4), 'R1.'))
        return phrase

    for _ in range(11):
        bell_voice.extend(make_bell_phrase())

    for _ in range(19):
        bell_voice.append(measuretools.Measure((6, 4), 'R1.'))

    bell_voice.append(measuretools.Measure((6,4), r"a'1. \laissezVibrer"))

