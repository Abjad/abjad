# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_version_every_package_01():
    r'''The status of the five material packages should be that
    there is nothing to version in performer_inventory/ but that
    the other four packges can version.
    This is the reason for both the 'Nothing to version ...'
    and the 'Will copy ...' messages showing up in the transcript.
    
    Test test differs from the corresponding test for SegmentPackageWrangler.
    The reason is that the artifact structure of the material packages
    is more complicated. So this test doesn't both actually touching
    the filesystem and just test messaging.
    '''
    
    input_ = 'red~example~score m vr* n q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Nothing to version ...' in contents
    assert 'Will copy ...' in contents