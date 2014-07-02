import os
from abjad import *
from output import magic_numbers


def __illustrate__(magic_numbers):
    strings = [str(_) for _ in magic_numbers]
    string = ' '.join(strings)
    markup = Markup(string)
    lilypond_file = lilypondfiletools.LilyPondFile()
    lilypond_file.items.append(markup)
    return lilypond_file