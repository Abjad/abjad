# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_ScorePackageProxy_read_only_attributes_01():
    r'''Read-only public attributes.
    '''

    score_proxy = scoremanagertools.proxies.ScorePackageProxy(
        'scoremanagertools.scorepackages.red_example_score')

    assert isinstance(
        score_proxy.segment_wrangler, 
        scoremanagertools.wranglers.SegmentPackageWrangler,
        )
    assert isinstance(
        score_proxy.distribution_directory_manager, 
        scoremanagertools.proxies.DirectoryManager,
        )
    assert isinstance(
        score_proxy.build_directory_manager, 
        scoremanagertools.proxies.DirectoryManager,
        )
    assert isinstance(
        score_proxy.material_package_maker_wrangler,
        scoremanagertools.wranglers.MaterialPackageMakerWrangler,
        )
    assert isinstance(
        score_proxy.material_package_wrangler,
        scoremanagertools.wranglers.MaterialPackageWrangler,
        )

    assert score_proxy._get_annotated_title() == 'Red Example Score (2013)'
    assert score_proxy._breadcrumb == 'Red Example Score (2013)'
    assert score_proxy.get_tag('composer') is None
    assert score_proxy.get_tag('title') == 'Red Example Score'
    assert score_proxy.get_tag('year_of_completion') == 2013

    assert score_proxy.top_level_directory_proxies == (
        scoremanagertools.proxies.DistributionDirectoryManager(
        'scoremanagertools.scorepackages.red_example_score'),
        scoremanagertools.proxies.BuildDirectoryManager(
        'scoremanagertools.scorepackages.red_example_score'),
        )
