import os
from experimental import *


def test_StylesheetFileProxy_rename_interactively_01():
    '''Nonversioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'stylesheets', 'test-stylesheet.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(filesystem_path=filesystem_path)
    assert not proxy.exists()

    try:
        proxy.make_empty_asset()
        assert proxy.exists()
        assert not proxy.is_versioned()
        new_filesystem_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path,
            'stylesheets', 'new-test-stylesheet.ly')
        proxy.interactively_rename(user_input='new-test-stylesheet.ly y q')
        assert proxy.filesystem_path == new_filesystem_path
        assert not os.path.exists(filesystem_path)
        assert os.path.exists(new_filesystem_path)
    finally:
        proxy.remove()
        assert not os.path.exists(filesystem_path)
        assert not os.path.exists(new_filesystem_path)


def test_StylesheetFileProxy_rename_interactively_02():
    '''Versioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'stylesheets', 'test-stylesheet.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        proxy.make_empty_asset()
        assert os.path.exists(filesystem_path)
        proxy.svn_add()
        assert proxy.is_versioned()
        new_filesystem_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path,
            'stylesheets', 'new-test-stylesheet.ly')
        proxy.interactively_rename(user_input='new-test-stylesheet.ly y q')
        assert proxy.filesystem_path == new_filesystem_path
        assert os.path.exists(new_filesystem_path)
    finally:
        proxy.remove()
        assert not os.path.exists(filesystem_path)
        assert not os.path.exists(new_filesystem_path)
