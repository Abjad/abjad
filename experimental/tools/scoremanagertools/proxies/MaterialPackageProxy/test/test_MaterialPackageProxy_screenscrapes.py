import py
from experimental import *


def test_MaterialPackageProxy_screenscrapes_01():
    '''Score material run from home.
    '''
    py.test.skip('TODO: add Red Example Score time signatures.')


    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(user_input='all red_example_score m black q')

    assert score_manager.transcript[-2] == \
    ['Red Example Score (2013) - materials - time signatures',
      '',
      '     material definition - edit (mde)',
      '     material definition - execute (mdx)',
      '',
      '     output material - make (omm)',
      '     output material - view (omv)',
      '',
      '     illustration builder - edit (ibe)',
      '     illustration builder - execute (ibx)',
      '     score stylesheet - select (sss)',
      '',
      '     output pdf - make (pdfm)',
      '     output pdf - view (pdfv)',
      '']


def test_MaterialPackageProxy_screenscrapes_02():
    '''Score material run independently.
    '''
    py.test.skip('TODO: add Red Example Score time signatures.')

    material_proxy = scoremanagertools.proxies.MaterialPackageProxy(
        'red_example_score.music.materials.time_signatures')
    material_proxy._run(user_input='q')

    assert material_proxy.transcript[-2] == \
    ['Time signatures',
      '',
      '     material definition - edit (mde)',
      '     material definition - execute (mdx)',
      '',
      '     output material - make (omm)',
      '     output material - view (omv)',
      '',
      '     illustration builder - edit (ibe)',
      '     illustration builder - execute (ibx)',
      '     score stylesheet - select (sss)',
      '',
      '     output pdf - make (pdfm)',
      '     output pdf - view (pdfv)',
      '']
