# -*- encoding: utf-8 -*-
import os
from abjad import *
from definition import segment_maker


lilypond_file = segment_maker()
current_directory = os.path.dirname(__file__)
pdf_file_path = os.path.join(current_directory, 'output.pdf')
persist(lilypond_file).as_pdf(pdf_file_path, candidacy=True)