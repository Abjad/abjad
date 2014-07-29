# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_display_every_asset_status_01():
    r'''Works with stylesheet library.
    '''

    input_ = 'yy rst* q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_StylesheetWrangler_display_every_asset_status_02():
    r'''Works with Git-managed score.
    '''

    input_ = 'red~example~score y rst* q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_StylesheetWrangler_display_every_asset_status_03():
    r'''Works with Subversion-managed score.
    '''

    # is_test=False to allow user scores to appear
    ide = scoremanager.idetools.AbjadIDE(is_test=False)
    score_name = ide._score_package_wrangler._find_svn_score_name()
    if not score_name:
        return

    input_ = '{} y rst* q'.format(score_name)
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents