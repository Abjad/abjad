# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__ScorePackageWrangler_views__.py',
    )


def test_ScorePackageWrangler_rename_view_01():

    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'vnew _test_100 rm all'
        input_ += ' add Red~Example~Score done <return> q' 
        score_manager._run(input_=input_)
            
        input_ = 'vae q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' in contents
        assert '_test_101' not in contents

        input_ = 'vren _test_100 _test_101 <return> q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents

        input_ = 'vae q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' not in contents
        assert '_test_101' in contents

        input_ = 'vrm _test_101 <return> q'
        score_manager._run(input_=input_)

        input_ = 'vae q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_101' not in contents