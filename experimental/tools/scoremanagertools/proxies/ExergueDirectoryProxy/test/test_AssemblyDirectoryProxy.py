import os
from experimental import *


def test_ExergueDirectoryProxy_01():

    exergue_directory_proxy = scoremanagertools.proxies.ExergueDirectoryProxy('example_score_1')

    assert exergue_directory_proxy.filesystem_path == os.path.join(
        exergue_directory_proxy.configuration.user_scores_directory_path, 'example_score_1', 'exergue')
    assert exergue_directory_proxy._spaced_class_name == 'exergue directory proxy'
