# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must have is_test=False to test views
score_manager = scoremanager.idetools.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__StylesheetWrangler_views__.py',
    )
metadata_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__metadata__.py',
    )


def test_StylesheetWrangler_set_view_01():
    r'''In library. Applies view.
    
    Makes sure only one stylesheet is visible after view is applied.
    '''
    
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'Y vnew _test rm all add clean-letter-14.ily done'
        input_ += ' vs _test q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        lines = [
            'Abjad IDE - stylesheets [_test]',
            '',
            '   1: clean-letter-14.ily (Abjad)',
            '',
            '      stylesheets - copy (cp)',
            '      stylesheets - new (new)',
            '      stylesheets - remove (rm)',
            '      stylesheets - rename (ren)',
            '',
            ]
        assert any(_.lines for _ in transcript)


def test_StylesheetWrangler_set_view_02():
    r'''In score package. Applies view.
    
    Makes sure only one stylesheet is visible after view is applied.
    '''
    
    views_file = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'stylesheets',
        '__views__.py',
        )
    metadata_file = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'stylesheets',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'red~example~score y vnew _test'
        input_ += ' rm all add stylesheet-addendum.ily done'
        input_ += ' vs _test q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        lines = [
            'Red Example Score (2013) - stylesheets [_test]',
            '',
            '   1: stylesheet-addendum.ily',
            '',
            '      stylesheets - copy (cp)',
            '      stylesheets - new (new)',
            '      stylesheets - remove (rm)',
            '      stylesheets - rename (ren)',
            '',
            ]
        assert any(_.lines for _ in transcript)