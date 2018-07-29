import abjad
import pathlib


def test_AbjadConfiguration___init___01():
    configuration = abjad.AbjadConfiguration()
    assert configuration.configuration_directory.exists()
    assert configuration.configuration_file_path.exists()
    assert pathlib.Path(configuration.abjad_output_directory).exists()
    for key in [
        'abjad_output_directory',
        'lilypond_path',
        'midi_player',
        'pdf_viewer',
        'text_editor',
    ]:
        assert key in configuration
