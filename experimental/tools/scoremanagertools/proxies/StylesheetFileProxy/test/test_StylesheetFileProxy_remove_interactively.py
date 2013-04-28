import os
from experimental import *


def test_StylesheetFileProxy_remove_interactively_01():
    '''Nonversioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    file_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'stylesheets', 'test_stylesheet.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(file_path=file_path)
    assert not proxy.exists

    try:
        proxy.conditionally_make_empty_asset()
        assert proxy.exists
        proxy.remove_interactively(user_input='remove default q')
        assert not proxy.exists
        assert not os.path.exists(file_path)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        assert not os.path.exists(file_path)


def test_StylesheetFileProxy_remove_interactively_02():
    '''Versioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    file_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'stylesheets', 'temporary_stylesheet.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(file_path=file_path)
    assert not proxy.exists

    try:
        proxy.conditionally_make_empty_asset()
        assert os.path.exists(file_path)
        proxy.svn_add()
        assert proxy.is_versioned
        proxy.remove_interactively(user_input='remove default q')
        assert not proxy.exists
        assert not os.path.exists(file_path)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        assert not os.path.exists(file_path)
