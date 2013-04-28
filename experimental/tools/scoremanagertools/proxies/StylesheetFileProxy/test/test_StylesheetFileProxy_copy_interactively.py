import os
from experimental import *


def test_StylesheetFileProxy_copy_interactively_01():

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    file_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'stylesheets', 'clean_letter_14.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(path=file_path)
    assert proxy.exists

    try:
        new_file_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path,
            'stylesheets', 'new_clean_letter_14.ly')
        proxy.copy_interactively(user_input='new_clean_letter_14 y default q')
        assert os.path.exists(file_path)
        assert os.path.exists(new_file_path)
        os.remove(new_file_path)
    finally:
        if os.path.exists(new_file_path):
            os.remove(new_file_path)
        assert os.path.exists(file_path)
        assert not os.path.exists(new_file_path)
