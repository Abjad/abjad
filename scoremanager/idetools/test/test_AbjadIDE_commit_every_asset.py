# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_commit_every_asset_01():

    ide._session._is_repository_test = True
    input_ = 'hh rci* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_commit