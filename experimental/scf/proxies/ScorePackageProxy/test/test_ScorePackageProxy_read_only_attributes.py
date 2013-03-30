# -*- encoding: utf-8 -*-
import os
from abjad.tools import instrumenttools
from abjad.tools import scoretools
import scf


def test_ScorePackageProxy_read_only_attributes_01():
    '''Read-only public attributes.
    '''

    score_proxy = scf.proxies.ScorePackageProxy('example_score_1')


    assert isinstance(score_proxy.chunk_wrangler, scf.wranglers.ChunkPackageWrangler)
    assert isinstance(score_proxy.dist_proxy, scf.proxies.DirectoryProxy)
    assert isinstance(score_proxy.etc_proxy, scf.proxies.DirectoryProxy)
    assert isinstance(score_proxy.exg_proxy, scf.proxies.DirectoryProxy)
    assert isinstance(score_proxy.material_package_maker_wrangler, scf.wranglers.MaterialPackageMakerWrangler)
    assert isinstance(score_proxy.material_package_wrangler, scf.wranglers.MaterialPackageWrangler)
    assert isinstance(score_proxy.mus_proxy, scf.proxies.MusPackageProxy)

    assert score_proxy.has_correct_initializers

    # TODO: create Example Score I instrumentation
#    instrumentation = scoretools.InstrumentationSpecifier()
#    performer_1 = scoretools.Performer('flutist')
#    performer_1.instruments.append(instrumenttools.AltoFlute())
#    instrumentation.performers.append(performer_1)
#    performer_2 = scoretools.Performer('guitarist')
#    performer_2.instruments.append(instrumenttools.Guitar())
#    instrumentation.performers.append(performer_2)

    assert score_proxy.annotated_title == 'Example Score I (2013)'
    assert score_proxy.breadcrumb == 'Example Score I (2013)'
    assert score_proxy.composer is None
    # TODO: create Example Score I instrumentation
    #assert score_proxy.instrumentation == instrumentation
    assert score_proxy.materials_package_importable_name == 'example_score_1.mus.materials'
    assert score_proxy.title == 'Example Score I'
    assert score_proxy.year_of_completion == 2013

    assert score_proxy.score_initializer_file_names == (
        os.path.join(os.environ.get('SCORES'), 'example_score_1', '__init__.py'),
        os.path.join(os.environ.get('SCORES'), 'example_score_1', 'mus', '__init__.py'))

    assert score_proxy.score_package_wranglers == (
        scf.wranglers.ChunkPackageWrangler(),
        scf.wranglers.MaterialPackageWrangler())

    assert score_proxy.top_level_directory_proxies == (
        scf.proxies.DistDirectoryProxy('example_score_1'),
        scf.proxies.EtcDirectoryProxy('example_score_1'),
        scf.proxies.ExgDirectoryProxy('example_score_1'),
        scf.proxies.MusPackageProxy('example_score_1'))
