from abjad.tools import rhythmmakertools
import scf


def test_PackageContentSelector_run_01():

    selector = scf.selectors.PackageContentSelector()
    selector.asset_container_package_importable_names = ['abjad.tools.rhythmmakertools']

    assert selector.run(user_input='note') == rhythmmakertools.NoteRhythmMaker
