import os
from experimental import *


def test_AssemblyDirectoryProxy_01():

    exg_proxy = scoremanagertools.proxies.AssemblyDirectoryProxy('example_score_1')

    assert exg_proxy.directory_path == os.path.join(
        exg_proxy.configuration.scores_directory_path, 'example_score_1', 'exg')
    assert exg_proxy._spaced_class_name == 'assembly directory proxy'
