import os
import py
from experimental import *


score_manager = scoremanagertools.scoremanager.ScoreManager()
wrangler = score_manager.material_package_wrangler
assert not wrangler.session.is_in_score


def test_MaterialPackageWrangler_iteration_01():
    '''Assets (all).
    '''

    assert 'red sargasso measures' in wrangler.list_asset_human_readable_names()
    assert 'red sargasso measures' not in wrangler.list_asset_human_readable_names(head='example_score_1')


def test_MaterialPackageWrangler_iteration_02():

    assert 'materials.red_sargasso_measures' in \
        wrangler.list_asset_package_paths()
    assert 'materials.red_sargasso_measures' not in \
        wrangler.list_asset_package_paths(head='example_score_1')


def test_MaterialPackageWrangler_iteration_03():

    assert os.path.join(wrangler.configuration.score_manager_materials_directory_path, 'red_notes') in \
        wrangler.list_asset_paths()
    assert os.path.join(wrangler.configuration.score_manager_materials_directory_path, 'red_notes') not in \
        wrangler.list_asset_paths(head='example_score_1')
    assert wrangler.list_asset_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_04():

    # wrangler.list_asset_proxies()
    pass


def test_MaterialPackageWrangler_iteration_05():
    '''Score-internal asset containers.
    '''

    assert 'example_score_1.mus.materials' in \
        wrangler.list_score_internal_asset_container_package_paths()
    assert 'example_score_2.mus.materials' in \
        wrangler.list_score_internal_asset_container_package_paths()
    assert 'example_score_1.mus.materials' not in \
        wrangler.list_score_internal_asset_container_package_paths(head='example_score_2')
    assert 'example_score_2.mus.materials' not in \
        wrangler.list_score_internal_asset_container_package_paths(head='example_score_1')
    assert wrangler.list_score_internal_asset_container_package_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_06():

    path = os.path.join(wrangler.configuration.scores_directory_path, 'example_score_1', 'mus', 'materials')
    assert path in wrangler.list_score_internal_asset_container_paths()
    assert path not in wrangler.list_score_internal_asset_container_paths(head='example_score_2')
    assert wrangler.list_score_internal_asset_container_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_07():
    '''Score-internal assets.
    '''
    py.test.skip('TODO: add time_signatures package to Example Score I.')

    assert 'example_score_1.mus.materials.time_signatures' in \
        wrangler.list_score_internal_asset_package_paths()
    assert 'example_score_1.mus.materials.time_signatures' not in \
        wrangler.list_score_internal_asset_package_paths(head='example_score_2')
    assert wrangler.list_score_internal_asset_package_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_08():
    py.test.skip('TODO: add time_signatures package to Example Score I.')

    path = os.path.join(
        wrangler.configuration.scores_directory_path, 
        'example_scores_1', 'mus', 'materials', 'time_signatures')
    assert path in wrangler.list_score_internal_asset_paths()
    assert path in wrangler.list_score_internal_asset_paths(head='example_score_2')
    assert wrangler.list_score_internal_asset_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_09():
    '''Visible assets.
    '''

    assert 'red sargasso measures' in wrangler.list_visible_asset_human_readable_names()
    assert 'red sargasso measures' not in wrangler.list_visible_asset_human_readable_names(head='example_score_1')
    assert wrangler.list_visible_asset_human_readable_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_10():
   py.test.skip('TODO: add time_signatures package to Example Score I.')

   assert 'example_score_1.mus.materials.time_signatures' in \
        wrangler.list_visible_asset_package_paths()
   assert 'example_score_1.mus.materials.time_signatures' not in \
        wrangler.list_visible_asset_package_paths(head='example_score_2')
   assert wrangler.list_visible_asset_package_paths(head='asdf') == []


def test_MaterialPackageWrangler_iteration_11():
    py.test.skip('TODO: add time_signatures package to Example Score I.')

    assert ('materials.red_sargasso_measures', 'red sargasso measures') in \
        wrangler.make_visible_asset_menu_tokens()
    assert ('example_score_1.mus.materials.time_signatures', 'time signatures') in \
        wrangler.make_visible_asset_menu_tokens()
    assert ('materials.red_sargasso_measures', 'red sargasso measures') not in \
        wrangler.make_visible_asset_menu_tokens(head='example_score_1')
    assert ('example_score_1.mus.materials.time_signatures', 'time signatures') not in \
        wrangler.make_visible_asset_menu_tokens(head='example_score_2')


def test_MaterialPackageWrangler_iteration_12():

    # wrangler.list_visible_asset_proxies()
    pass
