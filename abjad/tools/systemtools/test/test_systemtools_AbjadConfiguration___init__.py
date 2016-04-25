# -*- coding: utf-8 -*-
import os
from abjad import *


def test_systemtools_AbjadConfiguration___init___01():

    abjad_configuration = systemtools.AbjadConfiguration()

    assert os.path.exists(abjad_configuration.configuration_directory_path)
    assert os.path.exists(abjad_configuration.configuration_file_path)
    assert os.path.exists(abjad_configuration.abjad_output_directory)

    keys = [
        'abjad_output_directory',
        'accidental_spelling',
        'lilypond_path',
        'midi_player',
        'pdf_viewer',
        'text_editor',
        ]

    for key in keys:
        assert key in abjad_configuration
