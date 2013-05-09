from experimental import *


def test_SegmentPackageWrangler_read_only_attributes_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.segment_package_wrangler
    assert not wrangler.session.is_in_score

    assert wrangler.breadcrumb == 'sketches'
    assert wrangler.current_asset_container_package_path == 'sketches'
    assert all([x.startswith('sketches') for x in wrangler.list_score_external_asset_package_paths()])

    assert wrangler.list_system_asset_container_package_paths() == ['sketches']
    assert wrangler.score_internal_asset_container_path_infix_parts == ('music', 'segments')

    assert wrangler.temporary_asset_package_path == 'sketches.__temporary_package'

    assert 'sketches' in wrangler.list_asset_container_package_paths()
    assert 'example_score_1.music.segments' in wrangler.list_asset_container_package_paths()


def test_SegmentPackageWrangler_read_only_attributes_02():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.segment_package_wrangler
    wrangler.session.current_score_package_name = 'example_score_1'
    assert wrangler.session.is_in_score

    assert wrangler.breadcrumb == 'segments'

    assert wrangler.current_asset_container_package_path == 'example_score_1.music.segments'

    assert all([
        x.startswith('sketches.') for x in wrangler.list_score_external_asset_package_paths()])
    assert wrangler.list_system_asset_container_package_paths() == \
        ['sketches']

    assert wrangler.score_internal_asset_container_path_infix_parts == ('music', 'segments')

    assert wrangler.temporary_asset_package_path == 'example_score_1.music.segments.__temporary_package'

    assert 'sketches' in wrangler.list_asset_container_package_paths()
    assert 'example_score_1.music.segments' in wrangler.list_asset_container_package_paths()
