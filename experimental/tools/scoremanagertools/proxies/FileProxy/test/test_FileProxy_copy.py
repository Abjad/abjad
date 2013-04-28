import os
from experimental import *


def test_FileProxy_copy_01():

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    file_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'temporary_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(file_path=file_path)
    assert not os.path.exists(file_path)

    try:
        file_proxy.conditionally_make_empty_asset()
        assert os.path.exists(file_path)
        new_file_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path, 'new_temporary_file.txt')
        file_proxy.copy(new_file_path)
        assert os.path.exists(file_path)
        assert os.path.exists(new_file_path)
        file_proxy.remove()
        os.remove(new_file_path)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(new_file_path):
            os.remove(new_file_path)
        assert not os.path.exists(file_path)
        assert not os.path.exists(new_file_path)
