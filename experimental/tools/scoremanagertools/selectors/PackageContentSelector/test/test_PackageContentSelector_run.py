from abjad.tools import rhythmmakertools
from experimental import *


def test_PackageContentSelector_run_01():

    selector = scoremanagertools.selectors.PackageContentSelector()
    selector.asset_container_package_paths = ['abjad.tools.rhythmmakertools']

    assert selector.run(user_input='note') == rhythmmakertools.NoteRhythmMaker
