# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_DistributionDirectoryProxy_01():

    distribution_proxy = scoremanagertools.proxies.DistributionDirectoryProxy(
        'scoremanagertools.scorepackages.red_example_score')

    assert distribution_proxy.filesystem_path == os.path.join(
        distribution_proxy.configuration.built_in_score_packages_directory_path,
        'red_example_score', 'distribution')
    assert distribution_proxy._spaced_class_name == 'distribution directory proxy'
