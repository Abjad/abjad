# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__MakerFileWrangler_views__.py',
    )


def test_MakerFileWrangler_rename_view_01():
    r'''Works in library.
    '''

    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'K vnew _test_100 rm all'
        input_ += ' add RedExampleScoreTemplate.py~(Red~Example~Score)'
        input_ += ' done q' 
        score_manager._run(input_=input_)
            
        input_ = 'K va q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' in contents
        assert '_test_101' not in contents

        input_ = 'K vren _test_100 _test_101 q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents

        input_ = 'K va q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' not in contents
        assert '_test_101' in contents

        input_ = 'K vrm _test_101 q'
        score_manager._run(input_=input_)

        input_ = 'K va q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_101' not in contents