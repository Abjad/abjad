import os
from experimental import *


def test_FileProxy_copy_interactively_01():

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    path = os.path.join(
        score_manager_configuration.SCORE_MANAGER_TOOLS_DIRECTORY_PATH, 'temporary_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(path=path)
    assert not os.path.exists(path)

    try:
        file_proxy.conditionally_make_empty_asset()
        assert os.path.exists(path)
        new_path = os.path.join(
            score_manager_configuration.SCORE_MANAGER_TOOLS_DIRECTORY_PATH, 'new_temporary_file.txt')
        file_proxy.copy_interactively(user_input='new_temporary_file.txt y q')
        assert os.path.exists(path)
        assert os.path.exists(new_path)
        file_proxy.remove()
        os.remove(new_path)
    finally:
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists(new_path):
            os.remove(new_path)
        assert not os.path.exists(path)
        assert not os.path.exists(new_path)
