import os
import scf


def test_RhythmMakerPackageSelector_list_current_material_package_path_names_01():

    selector = scf.selectors.RhythmMakerPackageSelector()
    selector.session._current_score_package_short_name = 'betoerung'
    speckled_time_token_maker_path_name = os.path.join(
        os.environ.get('SCORES'), 'betoerung', 'mus', 'materials', 'speckled_time_token_maker')

    assert speckled_time_token_maker_path_name in selector.list_current_material_package_path_names()
