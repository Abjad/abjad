import os
from experimental import *


def test_StylesheetFileProxy_copy_interactively_01():

    path_name = os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'stylesheets', 'clean_letter_14.ly')
    proxy = scoremanagementtools.proxies.StylesheetFileProxy(path_name=path_name)
    assert proxy.exists

    try:
        new_path_name = os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'stylesheets', 'new_clean_letter_14.ly')
        proxy.copy_interactively(user_input='new_clean_letter_14 y default q')
        assert os.path.exists(path_name)
        assert os.path.exists(new_path_name)
        os.remove(new_path_name)
    finally:
        if os.path.exists(new_path_name):
            os.remove(new_path_name)
        assert os.path.exists(path_name)
        assert not os.path.exists(new_path_name)
