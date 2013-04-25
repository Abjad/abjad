import os
from experimental import *


def test_StylesheetFileProxy_copy_interactively_01():

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    path = os.path.join(
        score_manager_configuration.SCORE_MANAGER_TOOLS_DIRECTORY_PATH,
        'stylesheets', 'clean_letter_14.ly')
    proxy = scoremanagertools.proxies.StylesheetFileProxy(path=path)
    assert proxy.exists

    try:
        new_path = os.path.join(
            score_manager_configuration.SCORE_MANAGER_TOOLS_DIRECTORY_PATH,
            'stylesheets', 'new_clean_letter_14.ly')
        proxy.copy_interactively(user_input='new_clean_letter_14 y default q')
        assert os.path.exists(path)
        assert os.path.exists(new_path)
        os.remove(new_path)
    finally:
        if os.path.exists(new_path):
            os.remove(new_path)
        assert os.path.exists(path)
        assert not os.path.exists(new_path)
