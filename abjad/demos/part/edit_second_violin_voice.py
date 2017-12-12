import abjad


def edit_second_violin_voice(score, durated_reservoir):
    r'''Edits second violin voice.
    '''

    voice = score['Second Violin Voice']
    descents = durated_reservoir['Second Violin']

    last_descent = abjad.Selection(descents[-1])
    copied_descent = abjad.mutate(last_descent).copy()
    copied_descent = list(copied_descent)
    copied_descent[-1].written_duration = abjad.Duration(1, 1)
    copied_descent.append(abjad.Note('a2'))
    for leaf in copied_descent:
        articulation = abjad.Articulation('accent')
        abjad.attach(articulation, leaf)
        articulation = abjad.Articulation('tenuto')
        abjad.attach(articulation, leaf)
    voice.extend(copied_descent)

    final_sustain = []
    for _ in range(32):
        final_sustain.append(abjad.Note('a1.'))
    final_sustain.append(abjad.Note('a2'))
    final_sustain = abjad.Selection(final_sustain)
    articulation = abjad.Articulation('accent')
    abjad.attach(articulation, final_sustain[0])
    articulation = abjad.Articulation('tenuto')
    abjad.attach(articulation, final_sustain[0])

    voice.extend(final_sustain)
    tie = abjad.Tie()
    abjad.attach(tie, final_sustain)
    voice.extend('r4 r2.')
