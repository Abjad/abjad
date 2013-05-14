import os
from experimental import *


def test_ExergueDirectoryProxy_01():

    exergue_directory_proxy = scoremanagertools.proxies.ExergueDirectoryProxy(
        'scoremanagertools.built_in_scores.example_score_1')

    assert exergue_directory_proxy.filesystem_path == os.path.join(
        exergue_directory_proxy.configuration.score_manager_tools_directory_path, 
        'built_in_scores', 'example_score_1', 'exergue')
    assert exergue_directory_proxy._spaced_class_name == 'exergue directory proxy'
