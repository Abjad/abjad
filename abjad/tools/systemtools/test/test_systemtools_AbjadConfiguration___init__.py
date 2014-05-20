# -*- encoding: utf-8 -*-
import os
from abjad import *


def test_systemtools_AbjadConfiguration___init___01():

    ABJADCONFIG = systemtools.AbjadConfiguration()

    assert os.path.exists(ABJADCONFIG.abjad_configuration_directory)
    assert os.path.exists(ABJADCONFIG.abjad_configuration_file_path)
    assert os.path.exists(ABJADCONFIG.abjad_output_directory)

    keys = [
        'text_editor',
        'pdf_viewer',
        'lilypond_includes',
        'lilypond_path',
        'midi_player',
        'abjad_output_directory',
        'accidental_spelling',
        'lilypond_language',
    ]

    for key in keys:
        assert key in ABJADCONFIG