import os
from abjad import *
from output import magic_numbers


strings = [str(_) for _ in magic_numbers]
string = ' '.join(strings)
markup = Markup(string)

lilypond_file = lilypondfiletools.LilyPondFile()
lilypond_file.items.append(markup)

current_directory = os.path.dirname(__file__)
ly_file_path = os.path.join(current_directory, 'illustration.ly')
persist(lilypond_file).as_ly(ly_file_path)
pdf_file_path = os.path.join(current_directory, 'illustration.pdf')
persist(lilypond_file).as_pdf(pdf_file_path)