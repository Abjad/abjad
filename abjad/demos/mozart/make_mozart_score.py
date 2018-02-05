import abjad


def make_mozart_score():
    r'''Makes Mozart score.
    '''

    score_template = abjad.TwoStaffPianoScoreTemplate()
    score = score_template()

    # select the measures to use
    choices = abjad.demos.mozart.choose_mozart_measures()

    # create and populate the volta containers
    treble_volta = abjad.Container()
    bass_volta = abjad.Container()
    for choice in choices[:7]:
        treble, bass = abjad.demos.mozart.make_mozart_measure(choice)
        treble_volta.append(treble)
        bass_volta.append(bass)

    # abjad.attach indicators to the volta containers
    command = abjad.LilyPondCommand(
        'repeat volta 2', 'before'
        )
    abjad.attach(command, treble_volta)
    command = abjad.LilyPondCommand(
        'repeat volta 2', 'before'
        )
    abjad.attach(command, bass_volta)

    # append the volta containers to our staves
    score['RHVoice'].append(treble_volta)
    score['LHVoice'].append(bass_volta)

    # create and populate the alternative ending containers
    treble_alternative = abjad.Container()
    bass_alternative = abjad.Container()
    for choice in choices[7:9]:
        treble, bass = abjad.demos.mozart.make_mozart_measure(choice)
        treble_alternative.append(treble)
        bass_alternative.append(bass)

    # abjad.attach indicators to the alternative containers
    command = abjad.LilyPondCommand(
        'alternative', 'before'
        )
    abjad.attach(command, treble_alternative)
    command = abjad.LilyPondCommand(
        'alternative', 'before'
        )
    abjad.attach(command, bass_alternative)

    # append the alternative containers to our staves
    score['RHVoice'].append(treble_alternative)
    score['LHVoice'].append(bass_alternative)

    # create the remaining measures
    for choice in choices[9:]:
        treble, bass = abjad.demos.mozart.make_mozart_measure(choice)
        score['RHVoice'].append(treble)
        score['LHVoice'].append(bass)

    # abjad.attach indicators
    time_signature = abjad.TimeSignature((3, 8))
    leaf = abjad.inspect(score['RHStaff']).get_leaf(0)
    abjad.attach(time_signature, leaf)
    bar_line = abjad.BarLine('|.')
    leaf = abjad.inspect(score['RHStaff']).get_leaf(-1)
    abjad.attach(bar_line, leaf)
    bar_line = abjad.BarLine('|.')
    leaf = abjad.inspect(score['LHStaff']).get_leaf(-1)
    abjad.attach(bar_line, leaf)

    # remove the default piano instrument and add a custom one:
    abjad.detach(abjad.Instrument, score['PianoStaff'])
    klavier = abjad.instrumenttools.Piano(
        name='Katzenklavier',
        short_name='kk.',
        )
    leaf = abjad.inspect(score['PianoStaff']).get_leaf(0)
    abjad.attach(klavier, leaf)

    return score
