import os
from experimental import *


def test_DirectoryContentSelector_run_01():

    selector = scoremanagertools.selectors.DirectoryContentSelector()
    selector.asset_container_paths = [os.path.join(
        selector.configuration.abjad_configuration.ABJAD_DIRECTORY_PATH, 'tools', 'rhythmmakertools')]

    assert selector.run(user_input='note') == 'NoteRhythmMaker'
