# -*- encoding: utf-8 -*-
import os
from abjad import *
from output import PACKAGE_NAME


lilypond_file = PACKAGE_NAME.__illustrate__()
path = os.path.abspath(__file__)
directory = os.path.dirname(path)
path = os.path.join(directory, 'illustration.candidate.pdf')
persist(lilypond_file).as_pdf(candidate_path)