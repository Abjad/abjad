import os
import scf


def test_DirectoryContentSelector_run_01():

    selector = scf.selectors.DirectoryContentSelector()
    selector.asset_container_path_names = [os.path.join(os.environ.get('ABJAD'), 'tools', 'rhythmmakertools')]

    assert selector.run(user_input='note') == 'NoteRhythmMaker'
