import os
from experimental import *


def test_DirectoryContentSelector_run_01():

    selector = scoremanagertools.selectors.DirectoryContentSelector()
    selector.storehouse_filesystem_paths = [os.path.join(
        selector.configuration.abjad_configuration.abjad_directory_path, 'tools', 'rhythmmakertools')]

    assert selector._run(pending_user_input='note') == 'NoteRhythmMaker'
