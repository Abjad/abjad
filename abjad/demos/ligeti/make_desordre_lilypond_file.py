import abjad


def make_desordre_lilypond_file():
    '''Makes Désordre LilyPond file.
    '''
    pitches = abjad.demos.ligeti.make_desordre_pitches()
    score = abjad.demos.ligeti.make_desordre_score(pitches)
    package = abjad.documentationtools
    lilypond_file = package.make_ligeti_example_lilypond_file(score)
    return lilypond_file
