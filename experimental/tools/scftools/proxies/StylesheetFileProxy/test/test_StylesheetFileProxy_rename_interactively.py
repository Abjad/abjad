import os
from experimental import *


def test_StylesheetFileProxy_rename_interactively_01():
    '''Nonversioned file.
    '''

    path_name = os.path.join(os.environ.get('SCFPATH'), 'stylesheets', 'test_stylesheet.ly')
    proxy = scftools.proxies.StylesheetFileProxy(path_name=path_name)
    assert not proxy.exists

    try:
        proxy.conditionally_make_empty_asset()
        assert proxy.exists
        assert not proxy.is_versioned
        new_path_name = os.path.join(os.environ.get('SCFPATH'), 'stylesheets', 'new_test_stylesheet.ly')
        proxy.rename_interactively(user_input='new_test_stylesheet.ly y q')
        assert proxy.path_name == new_path_name
        assert not os.path.exists(path_name)
        assert os.path.exists(new_path_name)
    finally:
        proxy.remove()
        assert not os.path.exists(path_name)
        assert not os.path.exists(new_path_name)


def test_StylesheetFileProxy_rename_interactively_02():
    '''Versioned file.
    '''

    path_name = os.path.join(os.environ.get('SCFPATH'), 'stylesheets', 'test_stylesheet.ly')
    proxy = scftools.proxies.StylesheetFileProxy(path_name=path_name)
    assert not os.path.exists(path_name)

    try:
        proxy.conditionally_make_empty_asset()
        assert os.path.exists(path_name)
        proxy.svn_add()
        assert proxy.is_versioned
        new_path_name = os.path.join(os.environ.get('SCFPATH'), 'stylesheets', 'new_test_stylesheet.ly')
        proxy.rename_interactively(user_input='new_test_stylesheet.ly y q')
        assert proxy.path_name == new_path_name
        assert os.path.exists(new_path_name)
    finally:
        proxy.remove()
        assert not os.path.exists(path_name)
        assert not os.path.exists(new_path_name)
