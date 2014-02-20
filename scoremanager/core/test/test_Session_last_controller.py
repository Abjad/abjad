# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Session_last_controller_01():
    r'''Score manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='q')

    controller = score_manager._session.last_controller
    prototype = scoremanager.core.ScoreManager
    assert isinstance(controller, prototype)


def test_Session_last_controller_02():
    r'''Score package manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score q')

    controller = score_manager._session.last_controller
    prototype = scoremanager.managers.ScorePackageManager
    assert isinstance(controller, prototype)


def test_Session_last_controller_03():
    r'''Build directory manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score u q')

    controller = score_manager._session.last_controller
    prototype = scoremanager.managers.BuildDirectoryManager
    assert isinstance(controller, prototype)


def test_Session_last_controller_04():
    r'''Material package manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score m q')

    controller = score_manager._session.last_controller
    prototype = scoremanager.wranglers.MaterialPackageWrangler
    assert isinstance(controller, prototype)


def test_Session_last_controller_05():
    r'''Material package manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_user_input=string)

    controller = score_manager._session.last_controller
    prototype = scoremanager.managers.MaterialPackageManager
    assert isinstance(controller, prototype)


def test_Session_last_controller_06():
    r'''Segment wrangler.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score g q'
    score_manager._run(pending_user_input=string)

    controller = score_manager._session.last_controller
    prototype = scoremanager.wranglers.SegmentPackageWrangler
    assert isinstance(controller, prototype)


def test_Session_last_controller_07():
    r'''Segment package manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score g 1 q'
    score_manager._run(pending_user_input=string)

    controller = score_manager._session.last_controller
    prototype = scoremanager.managers.SegmentPackageManager
    assert isinstance(controller, prototype)


def test_Session_last_controller_08():
    r'''Segment package manager.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score g 1 q'
    score_manager._run(pending_user_input=string)

    controller = score_manager._session.last_controller
    prototype = scoremanager.managers.SegmentPackageManager
    assert isinstance(controller, prototype)


def test_Session_last_controller_09():
    r'''Stylesheet file wrangler.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score y q'
    score_manager._run(pending_user_input=string)

    controller = score_manager._session.last_controller
    prototype = scoremanager.wranglers.StylesheetFileWrangler
    assert isinstance(controller, prototype)
