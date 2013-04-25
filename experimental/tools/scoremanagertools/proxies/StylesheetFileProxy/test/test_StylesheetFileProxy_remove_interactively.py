import os
from experimental import *


def test_StylesheetFileProxy_remove_interactively_01():
    '''Nonversioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    path = os.path.join(
        score_manager_configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH,
        'stylesheets', 'test_stylesheet.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(path=path)
    assert not proxy.exists

    try:
        proxy.conditionally_make_empty_asset()
        assert proxy.exists
        proxy.remove_interactively(user_input='remove default q')
        assert not proxy.exists
        assert not os.path.exists(path)
    finally:
        if os.path.exists(path):
            os.remove(path)
        assert not os.path.exists(path)


def test_StylesheetFileProxy_remove_interactively_02():
    '''Versioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    path = os.path.join(
        score_manager_configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH,
        'stylesheets', 'temporary_stylesheet.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(path=path)
    assert not proxy.exists

    try:
        proxy.conditionally_make_empty_asset()
        assert os.path.exists(path)
        proxy.svn_add()
        assert proxy.is_versioned
        proxy.remove_interactively(user_input='remove default q')
        assert not proxy.exists
        assert not os.path.exists(path)
    finally:
        if os.path.exists(path):
            os.remove(path)
        assert not os.path.exists(path)
