import os
from experimental import *


def test_FileProxy_conditionally_make_empty_asset_01():

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, '__temporary_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_proxy.make_empty_asset()
        assert os.path.exists(filesystem_path)
        file_proxy.remove()
    finally:
        if os.path.exists(filesystem_path):
            os.remove(filesystem_path)
