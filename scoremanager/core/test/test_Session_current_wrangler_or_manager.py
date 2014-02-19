# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Session_current_wrangler_or_manager_01():
    r'''Score manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='q')

    result = score_manager.session.current_wrangler_or_manager
    prototype = scoremanager.core.ScoreManager
    assert isinstance(result, prototype)


def test_Session_current_wrangler_or_manager_02():
    r'''Score package manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score q')

    result = score_manager.session.current_wrangler_or_manager
    prototype = scoremanager.managers.ScorePackageManager
    assert isinstance(result, prototype)


def test_Session_current_wrangler_or_manager_03():
    r'''Build directory manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score u q')

    result = score_manager.session.current_wrangler_or_manager
    prototype = scoremanager.managers.BuildDirectoryManager
    assert isinstance(result, prototype)


def test_Session_current_wrangler_or_manager_04():
    r'''Material package manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score m q')

    result = score_manager.session.current_wrangler_or_manager
    prototype = scoremanager.wranglers.MaterialPackageWrangler
    assert isinstance(result, prototype)


def test_Session_current_wrangler_or_manager_05():
    r'''Material package manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_user_input=string)

    result = score_manager.session.current_wrangler_or_manager
    prototype = scoremanager.managers.MaterialPackageManager
    assert isinstance(result, prototype)


def test_Session_current_wrangler_or_manager_06():
    r'''Segment wrangler.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score g q'
    score_manager._run(pending_user_input=string)

    result = score_manager.session.current_wrangler_or_manager
    prototype = scoremanager.wranglers.SegmentPackageWrangler
    assert isinstance(result, prototype)


def test_Session_current_wrangler_or_manager_07():
    r'''Segment package manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score g 1 q'
    score_manager._run(pending_user_input=string)

    result = score_manager.session.current_wrangler_or_manager
    prototype = scoremanager.managers.SegmentPackageManager
    assert isinstance(result, prototype)


def test_Session_current_wrangler_or_manager_08():
    r'''Segment package manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score g 1 q'
    score_manager._run(pending_user_input=string)

    result = score_manager.session.current_wrangler_or_manager
    prototype = scoremanager.managers.SegmentPackageManager
    assert isinstance(result, prototype)


def test_Session_current_wrangler_or_manager_08():
    r'''Stylesheet file wrangler.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score y q'
    score_manager._run(pending_user_input=string)

    result = score_manager.session.current_wrangler_or_manager
    prototype = scoremanager.wranglers.StylesheetFileWrangler
    assert isinstance(result, prototype)
