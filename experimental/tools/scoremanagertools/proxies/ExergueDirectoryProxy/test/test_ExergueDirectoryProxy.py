import os
from experimental import *


def test_ExergueDirectoryProxy_01():

    exergue_directory_proxy = scoremanagertools.proxies.ExergueDirectoryProxy(
        'scoremanagertools.scorepackages.red_example_score')

    assert exergue_directory_proxy.filesystem_path == os.path.join(
        exergue_directory_proxy.configuration.score_manager_tools_directory_path, 
        'scorepackages', 'red_example_score', 'exergue')
    assert exergue_directory_proxy._spaced_class_name == 'exergue directory proxy'
