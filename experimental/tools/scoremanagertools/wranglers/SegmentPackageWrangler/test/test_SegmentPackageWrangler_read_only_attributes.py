from experimental import *


def test_SegmentPackageWrangler_read_only_attributes_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.segment_package_wrangler
    assert not wrangler._session.is_in_score

    assert wrangler._breadcrumb == 'sketches'
    assert wrangler.current_asset_container_packagesystem_path == 'sketches'

    assert wrangler._list_built_in_score_external_asset_container_packagesystem_path() == ['sketches']
    assert wrangler.asset_container_path_infix_parts == ('music', 'segments')

    assert wrangler._temporary_asset_package_path == 'sketches.__temporary_package'

    assert 'sketches' in wrangler._list_asset_container_package_paths()
    assert 'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.segments' \
        in wrangler._list_asset_container_package_paths()


def test_SegmentPackageWrangler_read_only_attributes_02():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.segment_package_wrangler
    wrangler._session.underscore_delimited_current_score_name = 'red_example_score'
    assert wrangler._session.is_in_score

    assert wrangler._breadcrumb == 'segments'

    assert wrangler.current_asset_container_packagesystem_path == \
        'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.segments'

    assert wrangler._list_built_in_score_external_asset_container_packagesystem_path() == \
        ['sketches']

    assert wrangler.asset_container_path_infix_parts == ('music', 'segments')

    assert wrangler._temporary_asset_package_path == \
        'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.segments.__temporary_package'

    assert 'sketches' in wrangler._list_asset_container_package_paths()
    assert 'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.segments' \
        in wrangler._list_asset_container_package_paths()
