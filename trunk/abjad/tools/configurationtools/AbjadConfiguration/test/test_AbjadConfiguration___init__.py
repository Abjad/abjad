from abjad.tools import configurationtools
import os


def test_AbjadConfiguration___init___01():

    ABJADCONFIG = configurationtools.AbjadConfiguration()

    assert os.path.exists(ABJADCONFIG.ABJAD_CONFIGURATION_DIRECTORY_PATH)
    assert os.path.exists(ABJADCONFIG.ABJAD_CONFIGURATION_FILE_PATH)
    assert os.path.exists(ABJADCONFIG.ABJAD_OUTPUT_DIRECTORY_PATH)

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
