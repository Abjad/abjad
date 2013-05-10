import os
from experimental import *

score_manager = scoremanagertools.scoremanager.ScoreManager()
wrangler = score_manager.material_package_wrangler
assert not wrangler.session.is_in_score


def test_MaterialPackageWrangler_read_only_attributes_01():
    '''Breadcrumb.
    '''

    assert wrangler.breadcrumb == 'materials'


def test_MaterialPackageWrangler_read_only_attributes_02():
    '''Asset containers (all).
    '''

    assert 'system_materials' in wrangler.list_asset_container_package_paths()
    assert 'example_score_1.music.materials' in wrangler.list_asset_container_package_paths()
    assert wrangler.configuration.system_materials_directory_path in \
        wrangler.list_asset_container_directory_paths()
    directory_path = os.path.join(
        wrangler.configuration.user_scores_directory_path, 'example_score_1', 'music', 'materials')
    assert directory_path in wrangler.list_asset_container_directory_paths()


def test_MaterialPackageWrangler_read_only_attributes_03():
    '''Current asset container.
    '''

    assert wrangler.current_asset_container_package_path == 'system_materials'
    assert wrangler.current_asset_container_directory_path == \
        wrangler.configuration.system_materials_directory_path


def test_MaterialPackageWrangler_read_only_attributes_04():
    '''Score-external asset container
    '''

    assert wrangler.list_system_asset_container_package_paths() == ['system_materials']
    assert wrangler.list_score_external_asset_container_directory_paths() == \
        [wrangler.configuration.system_materials_directory_path]


def test_MaterialPackageWrangler_read_only_attributes_05():
    '''Score-external assets.
    '''

    assert 'system_materials.red_notes' in wrangler.list_score_external_asset_package_paths()
    assert os.path.join(wrangler.configuration.system_materials_directory_path, 'red_notes') in \
        wrangler.list_score_external_asset_filesystem_paths()


def test_MaterialPackageWrangler_read_only_attributes_06():
    '''Infix.
    '''

    assert wrangler.asset_container_path_infix_parts == ('music', 'materials')


def test_MaterialPackageWrangler_read_only_attributes_07():
    '''Temporary asset.
    '''

    assert wrangler._temporary_asset_package_path == 'system_materials.__temporary_package'
    assert wrangler._temporary_asset_filesystem_path == \
        os.path.join(wrangler.configuration.system_materials_directory_path, '__temporary_package')
    assert wrangler._temporary_asset_name == '__temporary_package'


def test_MaterialPackageWrangler_read_only_attributes_08():
    '''In-score wrangler.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.material_package_wrangler
    wrangler.session.underscore_delimited_current_score_name = 'example_score_1'
    assert wrangler.session.is_in_score

    assert 'example_score_1.music.materials' in wrangler.list_asset_container_package_paths()
    assert wrangler.current_asset_container_package_path == 'example_score_1.music.materials'
    assert wrangler._temporary_asset_package_path == 'example_score_1.music.materials.__temporary_package'
    directory_path = os.path.join(
         wrangler.configuration.user_scores_directory_path,
        'example_score_1', 'music', 'materials', '__temporary_package')
    assert wrangler._temporary_asset_filesystem_path == directory_path
