from experimental import *


def test_SegmentPackageWrangler_read_only_attributes_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.segment_package_wrangler
    assert not wrangler._session.is_in_score

    assert wrangler._breadcrumb == 'segments'
    assert wrangler._current_storehouse_packagesystem_path is None

    assert wrangler.score_package_asset_storehouse_path_infix_parts == ('music', 'segments')

    assert wrangler._temporary_asset_package_path == '__temporary_package'

    assert 'experimental.tools.scoremanagertools.scorepackages.red_example_score.music.segments' \
        in wrangler._list_storehouse_package_paths()


def test_SegmentPackageWrangler_read_only_attributes_02():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.segment_package_wrangler
    wrangler._session.underscore_delimited_current_score_name = 'red_example_score'
    assert wrangler._session.is_in_score

    assert wrangler._breadcrumb == 'segments'

    assert wrangler._current_storehouse_packagesystem_path == \
        'experimental.tools.scoremanagertools.scorepackages.red_example_score.music.segments'

    assert wrangler.score_package_asset_storehouse_path_infix_parts == ('music', 'segments')

    assert wrangler._temporary_asset_package_path == \
        'experimental.tools.scoremanagertools.scorepackages.red_example_score.music.segments.__temporary_package'

    assert 'experimental.tools.scoremanagertools.scorepackages.red_example_score.music.segments' \
        in wrangler._list_storehouse_package_paths()
