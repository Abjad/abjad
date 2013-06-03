import os
from experimental import *


def test_StylesheetFileProxy_copy_interactively_01():

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'stylesheets', 'clean-letter-14.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(filesystem_path=filesystem_path)
    assert proxy.exists

    try:
        new_filesystem_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path,
            'stylesheets', 'new-clean-letter-14.ly')
        proxy.interactively_copy(user_input='new-clean-letter-14 y default q')
        assert os.path.exists(filesystem_path)
        assert os.path.exists(new_filesystem_path)
        os.remove(new_filesystem_path)
    finally:
        if os.path.exists(new_filesystem_path):
            os.remove(new_filesystem_path)
        assert os.path.exists(filesystem_path)
        assert not os.path.exists(new_filesystem_path)
