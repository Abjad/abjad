# -*- encoding: utf-8 -*-
from abjad import *
from abjad.demos.mozart.choose_mozart_measures import choose_mozart_measures
from abjad.demos.mozart.make_mozart_measure import make_mozart_measure


def make_mozart_score():

    score_template = scoretemplatetools.TwoStaffPianoScoreTemplate()
    score = score_template()

    # select the measures to use
    choices = choose_mozart_measures()

    # create and populate the volta containers
    treble_volta = Container()
    bass_volta = Container()
    for choice in choices[:7]:
        treble, bass = make_mozart_measure(choice)
        treble_volta.append(treble)
        bass_volta.append(bass)

    # attach indicators to the volta containers
    command = indicatortools.LilyPondCommand(
        'repeat volta 2', 'before'
        )
    attach(command, treble_volta)
    command = indicatortools.LilyPondCommand(
        'repeat volta 2', 'before'
        )
    attach(command, bass_volta)

    # append the volta containers to our staves
    score['RH Voice'].append(treble_volta)
    score['LH Voice'].append(bass_volta)

    # create and populate the alternative ending containers
    treble_alternative = Container()
    bass_alternative = Container()
    for choice in choices[7:9]:
        treble, bass = make_mozart_measure(choice)
        treble_alternative.append(treble)
        bass_alternative.append(bass)

    # attach indicators to the alternative containers
    command = indicatortools.LilyPondCommand(
        'alternative', 'before'
        )
    attach(command, treble_alternative)
    command = indicatortools.LilyPondCommand(
        'alternative', 'before'
        )
    attach(command, bass_alternative)

    # append the alternative containers to our staves
    score['RH Voice'].append(treble_alternative)
    score['LH Voice'].append(bass_alternative)

    # create the remaining measures
    for choice in choices[9:]:
        treble, bass = make_mozart_measure(choice)
        score['RH Voice'].append(treble)
        score['LH Voice'].append(bass)

    # attach indicators
    time_signature = indicatortools.TimeSignature((3, 8))
    attach(time_signature, score['RH Staff'])
    bar_line = indicatortools.BarLine('|.')
    attach(bar_line, score['RH Voice'][-1])
    bar_line = indicatortools.BarLine('|.')
    attach(bar_line, score['LH Voice'][-1])

    # remove the old, default piano instrument attached to the piano staff
    # and attach a custom instrument mark
    detach(instrumenttools.Instrument, score['Piano Staff'])

    klavier = instrumenttools.Piano(
        instrument_name='Katzenklavier', 
        short_instrument_name='kk.',
        )
    attach(klavier, score['Piano Staff'])

    return score
