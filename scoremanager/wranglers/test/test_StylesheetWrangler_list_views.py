# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__StylesheetWrangler_views__.py',
    )


def test_StylesheetWrangler_list_views_01():
    r'''Makes sure only one stylesheet is visible with view.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'y vls vnew _test rm all add clean-letter-14.ily done <return>'
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