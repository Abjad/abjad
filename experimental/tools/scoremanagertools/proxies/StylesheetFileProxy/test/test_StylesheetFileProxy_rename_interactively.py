import os
from experimental import *


def test_StylesheetFileProxy_rename_interactively_01():
    '''Nonversioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    file_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'built_in_stylesheets', 'test_stylesheet.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(file_path=file_path)
    assert not proxy.exists()

    try:
        proxy.make_empty_asset()
        assert proxy.exists()
        assert not proxy.is_versioned
        new_file_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path,
            'built_in_stylesheets', 'new_test_stylesheet.ly')
        proxy.rename_interactively(user_input='new_test_stylesheet.ly y q')
        assert proxy.file_path == new_file_path
        assert not os.path.exists(file_path)
        assert os.path.exists(new_file_path)
    finally:
        proxy.remove()
        assert not os.path.exists(file_path)
        assert not os.path.exists(new_file_path)


def test_StylesheetFileProxy_rename_interactively_02():
    '''Versioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    file_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'built_in_stylesheets', 'test_stylesheet.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(file_path=file_path)
    assert not os.path.exists(file_path)

    try:
        proxy.make_empty_asset()
        assert os.path.exists(file_path)
        proxy.svn_add()
        assert proxy.is_versioned
        new_file_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path,
            'built_in_stylesheets', 'new_test_stylesheet.ly')
        proxy.rename_interactively(user_input='new_test_stylesheet.ly y q')
        assert proxy.file_path == new_file_path
        assert os.path.exists(new_file_path)
    finally:
        proxy.remove()
        assert not os.path.exists(file_path)
        assert not os.path.exists(new_file_path)
