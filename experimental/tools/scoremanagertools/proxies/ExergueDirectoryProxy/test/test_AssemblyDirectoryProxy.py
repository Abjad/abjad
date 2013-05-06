import os
from experimental import *


def test_ExergueDirectoryProxy_01():

    assembly_proxy = scoremanagertools.proxies.ExergueDirectoryProxy('example_score_1')

    assert assembly_proxy.directory_path == os.path.join(
        assembly_proxy.configuration.scores_directory_path, 'example_score_1', 'assembly')
    assert assembly_proxy._spaced_class_name == 'exergue directory proxy'
