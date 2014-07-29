# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)
ide._session._is_repository_test = True


def test_MaterialPackageWrangler_update_every_asset_01():
    r'''Works in score.
    '''

    input_ = 'red~example~score m rup* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_update


def test_MaterialPackageWrangler_update_every_asset_02():
    r'''Works in library.
    '''

    input_ = 'mm rup* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_update