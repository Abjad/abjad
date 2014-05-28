# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__StylesheetWrangler_views__.py',
    )


def test_StylesheetWrangler_rename_view_01():
    r'''Works in library.
    '''

    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'y vnew _test_100 rm all add clean-letter-14.ily done <return> q' 
        score_manager._run(input_=input_)
            
        input_ = 'y vls q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' in contents
        assert '_test_101' not in contents

        input_ = 'y vren _test_100 _test_101 <return> q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents

        input_ = 'y vls q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' not in contents
        assert '_test_101' in contents

        input_ = 'y vrm _test_101 <return> q'
        score_manager._run(input_=input_)

        input_ = 'y vls q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_101' not in contents