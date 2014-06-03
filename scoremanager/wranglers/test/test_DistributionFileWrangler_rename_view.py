# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__DistributionFileWrangler_views__.py',
    )


def test_DistributionFileWrangler_rename_view_01():
    r'''Works in library.
    '''

    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'd vnew _test_100 rm all'
        input_ += ' add red-example-score.pdf~(Red~Example~Score) done'
        input_ += ' <return> q' 
        score_manager._run(input_=input_)
            
        input_ = 'd vls q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' in contents
        assert '_test_101' not in contents

        input_ = 'd vren _test_100 _test_101 <return> q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents

        input_ = 'd vls q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' not in contents
        assert '_test_101' in contents

        input_ = 'd vrm _test_101 <return> q'
        score_manager._run(input_=input_)

        input_ = 'd vls q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_101' not in contents