from abjad.tools import rhythmmakertools
from experimental import *


def test_PackageContentSelector_run_01():

    selector = scoremanagertools.selectors.PackageContentSelector()
    selector.storehouse_package_paths = ['abjad.tools.rhythmmakertools']

    assert selector._run(user_input='note') == rhythmmakertools.NoteRhythmMaker
