import abjad


def edit_first_violin_voice(score, durated_reservoir):
    r'''Edits first violin voice.
    '''

    voice = score['First Violin Voice']
    descents = durated_reservoir['First Violin']
    #descents = abjad.Selection(descents)

    last_descent = abjad.Selection(descents[-1])
    copied_descent = abjad.mutate(last_descent).copy()
    voice.extend(copied_descent)

    final_sustain_rhythm = [(6, 4)] * 43 + [(1, 2)]
    maker = abjad.NoteMaker()
    final_sustain_notes = maker(["c'"], final_sustain_rhythm)
    voice.extend(final_sustain_notes)
    tie = abjad.Tie()
    abjad.attach(tie, final_sustain_notes)
    voice.extend('r4 r2.')
