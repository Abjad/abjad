import os
from experimental import *


def test_StylesheetFileProxy_rename_interactively_01():
    '''Nonversioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'stylesheets', 'test_stylesheet.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(path=path)
    assert not proxy.exists

    try:
        proxy.conditionally_make_empty_asset()
        assert proxy.exists
        assert not proxy.is_versioned
        new_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path,
            'stylesheets', 'new_test_stylesheet.ly')
        proxy.rename_interactively(user_input='new_test_stylesheet.ly y q')
        assert proxy.path == new_path
        assert not os.path.exists(path)
        assert os.path.exists(new_path)
    finally:
        proxy.remove()
        assert not os.path.exists(path)
        assert not os.path.exists(new_path)


def test_StylesheetFileProxy_rename_interactively_02():
    '''Versioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'stylesheets', 'test_stylesheet.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(path=path)
    assert not os.path.exists(path)

    try:
        proxy.conditionally_make_empty_asset()
        assert os.path.exists(path)
        proxy.svn_add()
        assert proxy.is_versioned
        new_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path,
            'stylesheets', 'new_test_stylesheet.ly')
        proxy.rename_interactively(user_input='new_test_stylesheet.ly y q')
        assert proxy.path == new_path
        assert os.path.exists(new_path)
    finally:
        proxy.remove()
        assert not os.path.exists(path)
        assert not os.path.exists(new_path)
