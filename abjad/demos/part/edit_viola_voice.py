import abjad


def edit_viola_voice(score, durated_reservoir):
    r'''Edits viola voice.
    '''

    voice = score['Viola Voice']
    descents = durated_reservoir['Viola']

    for leaf in descents[-1]:
        articulation = abjad.Articulation('accent')
        abjad.attach(articulation, leaf)
        articulation = abjad.Articulation('tenuto')
        abjad.attach(articulation, leaf)
    last_descent = abjad.Selection(descents[-1])
    copied_descent = abjad.mutate(last_descent).copy()
    for leaf in copied_descent:
        if leaf.written_duration == abjad.Duration(4, 4):
            leaf.written_duration = abjad.Duration(8, 4)
        else:
            leaf.written_duration = abjad.Duration(4, 4)
    voice.extend(copied_descent)

    bridge = abjad.Note('e1')
    articulation = abjad.Articulation('tenuto')
    abjad.attach(articulation, bridge)
    articulation = abjad.Articulation('accent')
    abjad.attach(articulation, bridge)
    voice.append(bridge)

    final_sustain_rhythm = [(6, 4)] * 21 + [(1, 2)]
    maker = abjad.NoteMaker()
    final_sustain_notes = maker(['e'], final_sustain_rhythm)
    articulation = abjad.Articulation('accent')
    abjad.attach(articulation, final_sustain_notes[0])
    articulation = abjad.Articulation('tenuto')
    abjad.attach(articulation, final_sustain_notes[0])
    voice.extend(final_sustain_notes)
    tie = abjad.Tie()
    abjad.attach(tie, final_sustain_notes)
    voice.extend('r4 r2.')
