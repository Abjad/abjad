import os
import py
from experimental import *


score_manager = scoremanagertools.scoremanager.ScoreManager()
wrangler = score_manager.material_package_wrangler
assert not wrangler._session.is_in_score


def test_MaterialPackageWrangler_iteration_01():

    assert 'built_in_materials.red_sargasso_measures' in \
        wrangler.list_asset_package_paths()
    assert 'built_in_materials.red_sargasso_measures' not in \
        wrangler.list_asset_package_paths(
            head='experimental.tools.scoremanagertools.built_in_scores.example_score_1')


def test_MaterialPackageWrangler_iteration_02():

    assert os.path.join(wrangler.configuration.built_in_materials_directory_path, 'red_notes') in \
        wrangler.list_asset_filesystem_paths()
    assert os.path.join(wrangler.configuration.built_in_materials_directory_path, 'red_notes') not in \
        wrangler.list_asset_filesystem_paths(
            head='experimental.tools.scoremanagertools.built_in_scores.example_score_1')
    assert wrangler.list_asset_filesystem_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_03():
    '''Score-internal asset containers.
    '''

    assert 'experimental.tools.scoremanagertools.built_in_scores.example_score_1.music.materials' in \
        wrangler.list_score_internal_asset_container_package_paths()
    assert 'experimental.tools.scoremanagertools.built_in_scores.green_example_score.music.materials' in \
        wrangler.list_score_internal_asset_container_package_paths()
    assert 'experimental.tools.scoremanagertools.built_in_scores.example_score_1.music.materials' not in \
        wrangler.list_score_internal_asset_container_package_paths(
            head='experimental.tools.scoremanagertools.built_in_scores.green_example_score')
    assert 'experimental.tools.scoremanagertools.built_in_scores.green_example_score.music.materials' not in \
        wrangler.list_score_internal_asset_container_package_paths(
            head='experimental.tools.scoremanagertools.built_in_scores.example_score_1')
    assert wrangler.list_score_internal_asset_container_package_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_04():

    directory_path = os.path.join(
        wrangler.configuration.built_in_scores_directory_path, 'example_score_1', 'music', 'materials')
    assert directory_path in wrangler._list_score_internal_asset_container_directory_paths()
    assert directory_path not in wrangler._list_score_internal_asset_container_directory_paths(
        head='experimental.tools.scoremanagertools.built_in_scores.green_example_score')
    assert wrangler._list_score_internal_asset_container_directory_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_05():
    '''Score-internal assets.
    '''
    py.test.skip('TODO: add time_signatures package to Example Score I.')

    assert 'experimental.tools.scoremanagertools.built_in_scores.example_score_1.music.materials.time_signatures' in \
        wrangler.list_score_internal_asset_package_paths()
    assert 'experimental.tools.scoremanagertools.built_in_scores.example_score_1.music.materials.time_signatures' not in \
        wrangler.list_score_internal_asset_package_paths(
            head='experimental.tools.scoremanagertools.built_in_scores.green_example_score')
    assert wrangler.list_score_internal_asset_package_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_06():
    py.test.skip('TODO: add time_signatures package to Example Score I.')

    directory_path = os.path.join(
        wrangler.configuration.built_in_scores_directory_path,
        'example_scores_1', 'music', 'materials', 'time_signatures')
    assert directory_path in wrangler.list_score_internal_asset_filesystem_paths()
    assert directory_path in wrangler.list_score_internal_asset_filesystem_paths(
        head='experimental.tools.scoremanagertools.built_in_scores.green_example_score')
    assert wrangler.list_score_internal_asset_filesystem_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_07():
    '''Visible assets.
    '''

    assert 'red sargasso measures' in wrangler.list_space_delimited_lowercase_visible_asset_names()
    assert 'red sargasso measures' not in wrangler.list_space_delimited_lowercase_visible_asset_names(
        head='experimental.tools.scoremanagertools.built_in_scores.example_score_1')
    assert wrangler.list_space_delimited_lowercase_visible_asset_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_08():
   py.test.skip('TODO: add time_signatures package to Example Score I.')

   assert 'experimental.tools.scoremanagertools.built_in_scores.example_score_1.music.materials.time_signatures' in \
        wrangler.list_visible_asset_package_paths()
   assert 'experimental.tools.scoremanagertools.built_in_scores.example_score_1.music.materials.time_signatures' not in \
        wrangler.list_visible_asset_package_paths(
            head='experimental.tools.scoremanagertools.built_in_scores.green_example_score')
   assert wrangler.list_visible_asset_package_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_09():
    py.test.skip('TODO: add time_signatures package to Example Score I.')

    assert ('built_in_materials.red_sargasso_measures', 'red sargasso measures') in \
        wrangler._make_visible_asset_menu_tokens()
    assert ('example_score_1.music.materials.time_signatures', 'time signatures') in \
        wrangler._make_visible_asset_menu_tokens()
    assert ('built_in_materials.red_sargasso_measures', 'red sargasso measures') not in \
        wrangler._make_visible_asset_menu_tokens(head='example_score_1')
    assert ('example_score_1.music.materials.time_signatures', 'time signatures') not in \
        wrangler._make_visible_asset_menu_tokens(head='green_example_score')
