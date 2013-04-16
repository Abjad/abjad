import os
from experimental import *


def test_FileProxy_rename_01():
    '''Nonversioned file.
    '''

    path_name = os.path.join(os.environ.get('SCFPATH'), 'temporary_file.txt')
    file_proxy = scoremanagementtools.proxies.FileProxy(path_name=path_name)
    assert not os.path.exists(path_name)

    try:
        file_proxy.conditionally_make_empty_asset()
        assert os.path.exists(path_name)
        assert not file_proxy.is_versioned
        new_path_name = os.path.join(os.environ.get('SCFPATH'), 'new_temporary_file.txt')
        file_proxy.rename(new_path_name)
        assert not os.path.exists(path_name)
        assert os.path.exists(new_path_name)
        file_proxy.remove()
    finally:
        if os.path.exists(path_name):
            os.remove(path_name)
        if os.path.exists(new_path_name):
            os.remove(new_path_name)
        assert not os.path.exists(path_name)
        assert not os.path.exists(new_path_name)


def test_FileProxy_rename_02():
    '''Versioned file.
    '''

    path_name = os.path.join(os.environ.get('SCFPATH'), 'temporary_file.txt')
    file_proxy = scoremanagementtools.proxies.FileProxy(path_name=path_name)
    assert not os.path.exists(path_name)

    try:
        file_proxy.conditionally_make_empty_asset()
        assert os.path.exists(path_name)
        file_proxy.svn_add()
        assert file_proxy.is_versioned
        new_path_name = os.path.join(os.environ.get('SCFPATH'), 'new_temporary_file.txt')
        file_proxy.rename(new_path_name)
        assert os.path.exists(new_path_name)
        assert file_proxy.path_name == new_path_name
    finally:
        file_proxy.remove()
        assert not os.path.exists(path_name)
        assert not os.path.exists(new_path_name)
