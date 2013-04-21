import os
from experimental import *


def test_StylesheetFileProxy_remove_interactively_01():
    '''Nonversioned file.
    '''

    path_name = os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'stylesheets', 'test_stylesheet.ly')
    proxy = scoremanagementtools.proxies.StylesheetFileProxy(path_name=path_name)
    assert not proxy.exists

    try:
        proxy.conditionally_make_empty_asset()
        assert proxy.exists
        proxy.remove_interactively(user_input='remove default q')
        assert not proxy.exists
        assert not os.path.exists(path_name)
    finally:
        if os.path.exists(path_name):
            os.remove(path_name)
        assert not os.path.exists(path_name)


def test_StylesheetFileProxy_remove_interactively_02():
    '''Versioned file.
    '''

    path_name = os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'stylesheets', 'temporary_stylesheet.ly')
    proxy = scoremanagementtools.proxies.StylesheetFileProxy(path_name=path_name)
    assert not proxy.exists

    try:
        proxy.conditionally_make_empty_asset()
        assert os.path.exists(path_name)
        proxy.svn_add()
        assert proxy.is_versioned
        proxy.remove_interactively(user_input='remove default q')
        assert not proxy.exists
        assert not os.path.exists(path_name)
    finally:
        if os.path.exists(path_name):
            os.remove(path_name)
        assert not os.path.exists(path_name)
