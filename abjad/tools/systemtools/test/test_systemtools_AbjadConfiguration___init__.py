import abjad
import os
import pathlib
import pytest


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason="Travis-CI can not find configuration directory."
    )
def test_systemtools_AbjadConfiguration___init___01():

    configuration = abjad.AbjadConfiguration()

#    assert os.path.exists(configuration.configuration_directory)
#    assert os.path.exists(configuration.configuration_file_path)
#    assert os.path.exists(configuration.abjad_output_directory)
    assert configuration.configuration_directory.exists()
    assert configuration.configuration_file_path.exists()
    assert pathlib.Path(configuration.abjad_output_directory).exists()

    keys = [
        'abjad_output_directory',
        'accidental_spelling',
        'lilypond_path',
        'midi_player',
        'pdf_viewer',
        'text_editor',
        ]

    for key in keys:
        assert key in configuration
