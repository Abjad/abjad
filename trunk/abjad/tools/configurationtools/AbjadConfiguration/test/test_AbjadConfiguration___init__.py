from abjad.tools import configurationtools
import os


def test_AbjadConfiguration___init___01():

    ABJADCONFIG = configurationtools.AbjadConfiguration()

    assert os.path.exists(ABJADCONFIG.abjad_configuration_directory_path)
    assert os.path.exists(ABJADCONFIG.abjad_configuration_file_path)
    assert os.path.exists(ABJADCONFIG.abjad_output_directory_path)

    keys = [
        'text_editor',
        'pdf_viewer',
        'lilypond_includes',
        'lilypond_path',
        'midi_player',
        'abjad_output',
        'accidental_spelling',
        'lilypond_language',
    ]

    for key in keys:
        assert key in ABJADCONFIG
