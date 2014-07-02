# -*- encoding: utf-8 -*-
import os
from abjad import *
from output import OUTPUT_OBJECT
from __illustrate__ import __illustrate__


lilypond_file = __illustrate__(OUTPUT_OBJECT)
path = os.path.abspath(__file__)
directory = os.path.dirname(path)
candidate_path = os.path.join(directory, 'illustration.candidate.pdf')
persist(lilypond_file).as_pdf(candidate_path)