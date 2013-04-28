import os
from experimental import *


def test_FileProxy_conditionally_make_empty_asset_01():

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    file_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, '__temporary_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(path=file_path)
    assert not os.path.exists(file_path)

    try:
        file_proxy.conditionally_make_empty_asset()
        assert os.path.exists(file_path)
        file_proxy.remove()
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
