# -*- encoding: utf-8 -*-
import os
from abjad import *
from definition import segment_maker


lilypond_file = segment_maker()
current_directory = os.path.dirname(__file__)
candidate_path = os.path.join(current_directory, 'illustration.candidate.pdf')
persist(lilypond_file).as_pdf(candidate_path)