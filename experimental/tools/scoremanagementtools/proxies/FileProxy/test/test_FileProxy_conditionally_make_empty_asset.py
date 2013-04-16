import os
from experimental import *


def test_FileProxy_conditionally_make_empty_asset_01():

    path_name = os.path.join(os.environ.get('SCFPATH'), '__temporary_file.txt')
    file_proxy = scoremanagementtools.proxies.FileProxy(path_name=path_name)
    assert not os.path.exists(path_name)

    try:
        file_proxy.conditionally_make_empty_asset()
        assert os.path.exists(path_name)
        file_proxy.remove()
    finally:
        if os.path.exists(path_name):
            os.remove(path_name)
