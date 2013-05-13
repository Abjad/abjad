import os
from experimental import *


def test_StylesheetFileProxy_remove_interactively_01():
    '''Nonversioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'built_in_stylesheets', 'test_stylesheet.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(filesystem_path=filesystem_path)
    assert not proxy.exists()

    try:
        proxy.make_empty_asset()
        assert proxy.exists()
        proxy.remove_interactively(user_input='remove default q')
        assert not proxy.exists()
        assert not os.path.exists(filesystem_path)
    finally:
        if os.path.exists(filesystem_path):
            os.remove(filesystem_path)
        assert not os.path.exists(filesystem_path)


def test_StylesheetFileProxy_remove_interactively_02():
    '''Versioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'built_in_stylesheets', 'temporary_stylesheet.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(filesystem_path=filesystem_path)
    assert not proxy.exists()

    try:
        proxy.make_empty_asset()
        assert os.path.exists(filesystem_path)
        proxy.svn_add()
        assert proxy.is_versioned()
        proxy.remove_interactively(user_input='remove default q')
        assert not proxy.exists()
        assert not os.path.exists(filesystem_path)
    finally:
        if os.path.exists(filesystem_path):
            os.remove(filesystem_path)
        assert not os.path.exists(filesystem_path)
