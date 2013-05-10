import os
import py
from experimental import *


score_manager = scoremanagertools.scoremanager.ScoreManager()
wrangler = score_manager.material_package_wrangler
assert not wrangler._session.is_in_score


def test_MaterialPackageWrangler_iteration_01():
    '''Assets (all).
    '''

    assert 'red sargasso measures' in wrangler.list_space_delimited_lowercase_asset_names()
    assert 'red sargasso measures' not in wrangler.list_space_delimited_lowercase_asset_names(
        head='example_score_1')


def test_MaterialPackageWrangler_iteration_02():

    assert 'system_materials.red_sargasso_measures' in \
        wrangler.list_asset_package_paths()
    assert 'system_materials.red_sargasso_measures' not in \
        wrangler.list_asset_package_paths(head='example_score_1')


def test_MaterialPackageWrangler_iteration_03():

    assert os.path.join(wrangler.configuration.system_materials_directory_path, 'red_notes') in \
        wrangler.list_asset_filesystem_paths()
    assert os.path.join(wrangler.configuration.system_materials_directory_path, 'red_notes') not in \
        wrangler.list_asset_filesystem_paths(head='example_score_1')
    assert wrangler.list_asset_filesystem_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_04():

    # wrangler.list_asset_proxies()
    pass


def test_MaterialPackageWrangler_iteration_05():
    '''Score-internal asset containers.
    '''

    assert 'example_score_1.music.materials' in \
        wrangler.list_score_internal_asset_container_package_paths()
    assert 'example_score_2.music.materials' in \
        wrangler.list_score_internal_asset_container_package_paths()
    assert 'example_score_1.music.materials' not in \
        wrangler.list_score_internal_asset_container_package_paths(head='example_score_2')
    assert 'example_score_2.music.materials' not in \
        wrangler.list_score_internal_asset_container_package_paths(head='example_score_1')
    assert wrangler.list_score_internal_asset_container_package_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_06():

    directory_path = os.path.join(
        wrangler.configuration.user_scores_directory_path, 'example_score_1', 'music', 'materials')
    assert directory_path in wrangler.list_score_internal_asset_container_directory_paths()
    assert directory_path not in wrangler.list_score_internal_asset_container_directory_paths(head='example_score_2')
    assert wrangler.list_score_internal_asset_container_directory_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_07():
    '''Score-internal assets.
    '''
    py.test.skip('TODO: add time_signatures package to Example Score I.')

    assert 'example_score_1.music.materials.time_signatures' in \
        wrangler.list_score_internal_asset_package_paths()
    assert 'example_score_1.music.materials.time_signatures' not in \
        wrangler.list_score_internal_asset_package_paths(head='example_score_2')
    assert wrangler.list_score_internal_asset_package_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_08():
    py.test.skip('TODO: add time_signatures package to Example Score I.')

    directory_path = os.path.join(
        wrangler.configuration.user_scores_directory_path,
        'example_scores_1', 'music', 'materials', 'time_signatures')
    assert directory_path in wrangler.list_score_internal_asset_filesystem_paths()
    assert directory_path in wrangler.list_score_internal_asset_filesystem_paths(head='example_score_2')
    assert wrangler.list_score_internal_asset_filesystem_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_09():
    '''Visible assets.
    '''

    assert 'red sargasso measures' in wrangler.list_space_delimited_lowercase_visible_asset_names()
    assert 'red sargasso measures' not in wrangler.list_space_delimited_lowercase_visible_asset_names(head='example_score_1')
    assert wrangler.list_space_delimited_lowercase_visible_asset_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_10():
   py.test.skip('TODO: add time_signatures package to Example Score I.')

   assert 'example_score_1.music.materials.time_signatures' in \
        wrangler.list_visible_asset_package_paths()
   assert 'example_score_1.music.materials.time_signatures' not in \
        wrangler.list_visible_asset_package_paths(head='example_score_2')
   assert wrangler.list_visible_asset_package_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_11():
    py.test.skip('TODO: add time_signatures package to Example Score I.')

    assert ('system_materials.red_sargasso_measures', 'red sargasso measures') in \
        wrangler._make_visible_asset_menu_tokens()
    assert ('example_score_1.music.materials.time_signatures', 'time signatures') in \
        wrangler._make_visible_asset_menu_tokens()
    assert ('system_materials.red_sargasso_measures', 'red sargasso measures') not in \
        wrangler._make_visible_asset_menu_tokens(head='example_score_1')
    assert ('example_score_1.music.materials.time_signatures', 'time signatures') not in \
        wrangler._make_visible_asset_menu_tokens(head='example_score_2')


def test_MaterialPackageWrangler_iteration_12():

    # wrangler.list_visible_asset_proxies()
    pass
