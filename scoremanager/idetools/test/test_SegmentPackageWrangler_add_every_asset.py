# -*- encoding: utf-8 -*-
import pytest
import scoremanager


def test_SegmentPackageWrangler_add_every_asset_01():
    r'''Flow control reaches method in score.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    ide._session._is_repository_test = True
    input_ = 'red~example~score g rad* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_add


def test_SegmentPackageWrangler_add_every_asset_02():
    r'''Flow control reaches method in library.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    ide._session._is_repository_test = True
    input_ = 'gg rad* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_add