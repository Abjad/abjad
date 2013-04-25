import os
from experimental import *


def test_FileProxy_conditionally_make_empty_asset_01():

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    path = os.path.join(
        score_manager_configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH, '__temporary_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(path=path)
    assert not os.path.exists(path)

    try:
        file_proxy.conditionally_make_empty_asset()
        assert os.path.exists(path)
        file_proxy.remove()
    finally:
        if os.path.exists(path):
            os.remove(path)
