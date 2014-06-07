# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must set is_test=False for view tests
score_manager = scoremanager.core.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__StylesheetWrangler_views__.py',
    )


def test_StylesheetWrangler_rename_view_01():
    r'''Works in library.
    '''

    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'y vnew _test_100 rm all'
        input_ += ' add clean-letter-14.ily done <return> q' 
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


def test_StylesheetWrangler_rename_view_02():
    r'''Menu titles are good during rename.
    '''

    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'y vnew _test rm all add clean-letter-14.ily done'
        input_ += ' vap _test vren _test _fancy_test q'
        score_manager._run(input_=input_)

    titles =  [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets',
        'Abjad IDE - stylesheets - views - _test (EDIT)',
        'Abjad IDE - stylesheets - views - _test (EDIT)',
        'Abjad IDE - stylesheets - views - _test (EDIT)',
        'Abjad IDE - stylesheets',
        'Abjad IDE - stylesheets (_test)',
        'Abjad IDE - stylesheets (_test)',
        'Abjad IDE - stylesheets (_fancy_test)',
        ]
    assert score_manager._transcript.titles == titles