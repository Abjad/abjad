import abjad
import math


def make_desordre_cell(pitches):
    '''Makes a Désordre cell.
    '''

    notes = [abjad.Note(pitch, (1, 8)) for pitch in pitches]
    notes = abjad.Selection(notes)
    beam = abjad.Beam()
    abjad.attach(beam, notes)
    slur = abjad.Slur()
    abjad.attach(slur, notes)
    clef = abjad.Dynamic('f')
    abjad.attach(clef, notes[0])
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, notes[1])

    # make the lower voice
    lower_voice = abjad.Voice(notes)
    lower_voice.name = 'RH Lower Voice'
    command = abjad.LilyPondCommand('voiceTwo')
    abjad.attach(command, lower_voice)
    n = int(math.ceil(len(pitches) / 2.))
    chord = abjad.Chord([pitches[0], pitches[0] + 12], (n, 8))
    articulation = abjad.Articulation('>')
    abjad.attach(articulation, chord)

    # make the upper voice
    upper_voice = abjad.Voice([chord])
    upper_voice.name = 'RH Upper Voice'
    command = abjad.LilyPondCommand('voiceOne')
    abjad.attach(command, upper_voice)

    # combine them together
    container = abjad.Container([lower_voice, upper_voice])
    container.is_simultaneous = True

    # make all 1/8 beats breakable
    leaves = abjad.select(lower_voice).leaves()
    for leaf in leaves[:-1]:
        bar_line = abjad.BarLine('')
        abjad.attach(bar_line, leaf)

    return container
