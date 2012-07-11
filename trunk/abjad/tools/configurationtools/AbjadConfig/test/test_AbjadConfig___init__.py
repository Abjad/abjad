from abjad.tools import configurationtools
import os


def test_AbjadConfig___init___01():

    ABJADCONFIG = configurationtools.AbjadConfig()

    assert os.path.exists(ABJADCONFIG.ABJAD_CONFIG_DIRECTORY_PATH)
    assert os.path.exists(ABJADCONFIG.ABJAD_CONFIG_FILE_PATH)
    assert os.path.exists(ABJADCONFIG.ABJAD_OUTPUT_PATH)

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
