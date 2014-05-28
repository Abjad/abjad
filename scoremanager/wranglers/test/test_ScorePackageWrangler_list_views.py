# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__ScorePackageWrangler_views__.py',
    )


def test_ScorePackageWrangler_list_views_01():
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'vls vnew _test rm all'
        input_ += ' add Red~Example~Score done <return>'
        input_ += ' vls vrm _test <return> vls q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

        view_list_entries = [
            _ for _ in transcript
            if ('found' in _.contents or 'found' in _.contents)
            ]
        assert len(view_list_entries) == 3

        assert '_test' not in view_list_entries[0].contents
        assert '_test' in view_list_entries[1].contents
        assert '_test' not in view_list_entries[2].contents