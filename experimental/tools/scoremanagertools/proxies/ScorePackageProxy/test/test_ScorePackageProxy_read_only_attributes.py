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
        score_proxy.distribution_proxy, 
        scoremanagertools.proxies.DirectoryProxy,
        )
    assert isinstance(
        score_proxy.build_directory_manager, 
        scoremanagertools.proxies.DirectoryProxy,
        )
    assert isinstance(
        score_proxy.material_package_maker_wrangler,
        scoremanagertools.wranglers.MaterialPackageMakerWrangler,
        )
    assert isinstance(
        score_proxy.material_package_wrangler,
        scoremanagertools.wranglers.MaterialPackageWrangler,
        )

    assert score_proxy.has_correct_initializers

    # TODO: create Red Example Score instrumentation
#    instrumentation = scoretools.InstrumentationSpecifier()
#    performer_1 = scoretools.Performer('flutist')
#    performer_1.instruments.append(instrumenttools.AltoFlute())
#    instrumentation.performers.append(performer_1)
#    performer_2 = scoretools.Performer('guitarist')
#    performer_2.instruments.append(instrumenttools.Guitar())
#    instrumentation.performers.append(performer_2)

    assert score_proxy.annotated_title == 'Red Example Score (2013)'
    assert score_proxy._breadcrumb == 'Red Example Score (2013)'
    assert score_proxy.composer is None
    # TODO: create Red Example Score instrumentation
    #assert score_proxy.instrumentation == instrumentation
    assert score_proxy.materials_package_path == \
        'experimental.tools.scoremanagertools.scorepackages.red_example_score.materials'
    assert score_proxy.title == 'Red Example Score'
    assert score_proxy.year_of_completion == 2013

    directory_path = score_proxy.configuration.built_in_score_packages_directory_path
    assert score_proxy.score_initializer_file_names == (
        os.path.join(directory_path, 'red_example_score', '__init__.py'),
        )

    assert score_proxy.score_package_wranglers == (
        scoremanagertools.wranglers.SegmentPackageWrangler(),
        scoremanagertools.wranglers.MaterialPackageWrangler())

    assert score_proxy.top_level_directory_proxies == (
        scoremanagertools.proxies.DistributionDirectoryProxy(
            'scoremanagertools.scorepackages.red_example_score'),
        scoremanagertools.proxies.BuildDirectoryManager(
            'scoremanagertools.scorepackages.red_example_score'),
        )
