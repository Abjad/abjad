import abjad


def apply_rehearsal_marks(score):
    r'''Applies rehearsal marks to score.
    '''

    bell_voice = score['Bell Voice']

    measure_indices = [
        6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84,
        90, 96, 102,
        ]

    for measure_index in measure_indices:
        command = abjad.LilyPondCommand(r'mark \default', 'before')
        abjad.attach(command, bell_voice[measure_index])
