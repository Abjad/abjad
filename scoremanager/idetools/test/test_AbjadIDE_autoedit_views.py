# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__AbjadIDE_views__.py',
    )
metadata_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__metadata__.py',
    )


def test_AbjadIDE_autoedit_views_01():

    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)

        input_ = 'U vnew _test_100 rm all'
        input_ += ' add score.pdf~(Red~Example~Score) done q' 
        score_manager._run(input_=input_)
            
        input_ = 'U va q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' in contents
        assert '_test_101' not in contents

        input_ = 'U vren _test_100 _test_101 q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents

        input_ = 'U va q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' not in contents
        assert '_test_101' in contents

        input_ = 'U vrm _test_101 q'
        score_manager._run(input_=input_)

        input_ = 'U va q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_101' not in contents