# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# ok to have is_test=True to test view rename
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__SegmentPackageWrangler_views__.py',
    )


def test_SegmentPackageWrangler_rename_view_01():

    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'G vnew _test_100 rm all'
        input_ += ' add A~(Red~Example~Score) done q' 
        score_manager._run(input_=input_)
            
        input_ = 'G va q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' in contents
        assert '_test_101' not in contents

        input_ = 'G vren _test_100 _test_101 q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents

        input_ = 'G va q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' not in contents
        assert '_test_101' in contents

        input_ = 'G vrm _test_101 q'
        score_manager._run(input_=input_)

        input_ = 'G va q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_101' not in contents