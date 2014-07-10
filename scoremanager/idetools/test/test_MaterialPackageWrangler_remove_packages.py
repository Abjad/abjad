# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_remove_packages_01():

    ide._session._is_repository_test = True
    input_ = 'red~example~score m rm q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_remove