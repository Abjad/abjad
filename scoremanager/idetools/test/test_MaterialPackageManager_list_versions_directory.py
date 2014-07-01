# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageManager_list_versions_directory_01():

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m magic~numbers vl q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    string = 'definition_0001.py output_0001.py'
    assert string in contents

    
def test_MaterialPackageManager_list_versions_directory_02():

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m tempo~inventory vl q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    string = 'illustration_0001.ly illustration_0001.pdf output_0001.py'
    assert string in contents