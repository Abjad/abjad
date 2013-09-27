# -*- encoding: utf-8 -*-
import py
from experimental import *


def test_MaterialPackageManager_screenscrapes_01():
    r'''Score material run from home.
    '''
    py.test.skip('TODO: add Red Example Score time signatures.')


    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='all red_example_score m black q')

    assert score_manager.io_transcript[-2] == \
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


def test_MaterialPackageManager_screenscrapes_02():
    r'''Score material run independently.
    '''
    py.test.skip('TODO: add Red Example Score time signatures.')

    material_proxy = scoremanagertools.proxies.MaterialPackageManager(
        'red_example_score.materials.time_signatures')
    material_proxy._run(pending_user_input='q')

    assert material_proxy.io_transcript[-2] == \
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
