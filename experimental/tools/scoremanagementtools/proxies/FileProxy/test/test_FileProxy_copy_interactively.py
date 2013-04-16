import os
from experimental import *


def test_FileProxy_copy_interactively_01():

    path_name = os.path.join(os.environ.get('SCFPATH'), 'temporary_file.txt')
    file_proxy = scoremanagementtools.proxies.FileProxy(path_name=path_name)
    assert not os.path.exists(path_name)

    try:
        file_proxy.conditionally_make_empty_asset()
        assert os.path.exists(path_name)
        new_path_name = os.path.join(os.environ.get('SCFPATH'), 'new_temporary_file.txt')
        file_proxy.copy_interactively(user_input='new_temporary_file.txt y q')
        assert os.path.exists(path_name)
        assert os.path.exists(new_path_name)
        file_proxy.remove()
        os.remove(new_path_name)
    finally:
        if os.path.exists(path_name):
            os.remove(path_name)
        if os.path.exists(new_path_name):
            os.remove(new_path_name)
        assert not os.path.exists(path_name)
        assert not os.path.exists(new_path_name)
