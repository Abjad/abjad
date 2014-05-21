# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()

score_package_path = os.path.join(
    configuration.example_score_packages_directory,
    'red_example_score',
    )
tempo_inventory_package_path = os.path.join(
    score_package_path,
    'tempo_inventory',
    )
segment_package_path = os.path.join(
    score_package_path,
    'segments',
    'segment_01',
    )


def test_Session_controllers_visited_01():
    r'''Score manager.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'q'
    score_manager._run(pending_input=input_)

    session = scoremanager.core.Session(is_test=True)
    controllers = [
        scoremanager.core.ScoreManager(session=session, is_test=True),
        scoremanager.wranglers.ScorePackageWrangler(session=session),
        scoremanager.iotools.Menu(session=session),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_02():
    r'''Score package manager.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score q'
    score_manager._run(pending_input=input_)

    session = scoremanager.core.Session(is_test=True)
    controllers = [
        scoremanager.core.ScoreManager(session=session, is_test=True),
        scoremanager.wranglers.ScorePackageWrangler(session=session),
        scoremanager.iotools.Menu(session=session),
        scoremanager.managers.ScorePackageManager(
            path=score_package_path,
            session=session,
            ),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_03():
    r'''Build file wrangler.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score u q'
    score_manager._run(pending_input=input_)

    session = scoremanager.core.Session(is_test=True)
    controllers = [
        scoremanager.core.ScoreManager(session=session, is_test=True),
        scoremanager.wranglers.ScorePackageWrangler(session=session),
        scoremanager.iotools.Menu(session=session),
        scoremanager.managers.ScorePackageManager(
            session=session,
            path=score_package_path,
            ),
        scoremanager.wranglers.BuildFileWrangler(session=session),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_04():
    r'''Material package manager.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m q'
    score_manager._run(pending_input=input_)

    session = scoremanager.core.Session(is_test=True)
    controllers = [
        scoremanager.core.ScoreManager(session=session, is_test=True),
        scoremanager.wranglers.ScorePackageWrangler(session=session),
        scoremanager.iotools.Menu(session=session),
        scoremanager.managers.ScorePackageManager(
            path=score_package_path,
            session=session,
            ),
        scoremanager.wranglers.MaterialPackageWrangler(session=session),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_05():
    r'''Material package manager.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_input=input_)

    session = scoremanager.core.Session(is_test=True)
    controllers = [
        scoremanager.core.ScoreManager(session=session, is_test=True),
        scoremanager.wranglers.ScorePackageWrangler(session=session),
        scoremanager.iotools.Menu(session=session),
        scoremanager.managers.ScorePackageManager(
            path=score_package_path,
            session=session,
            ),
        scoremanager.wranglers.MaterialPackageWrangler(session=session),
        scoremanager.managers.MaterialPackageManager(
            path=tempo_inventory_package_path,
            session=session,
            ),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_06():
    r'''Segment wrangler.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score g q'
    score_manager._run(pending_input=input_)

    session = scoremanager.core.Session(is_test=True)
    controllers = [
        scoremanager.core.ScoreManager(session=session, is_test=True),
        scoremanager.wranglers.ScorePackageWrangler(session=session),
        scoremanager.iotools.Menu(session=session),
        scoremanager.managers.ScorePackageManager(
            path=score_package_path,
            session=session,
            ),
        scoremanager.wranglers.SegmentPackageWrangler(session=session),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_07():
    r'''Segment package manager.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score g 1 q'
    score_manager._run(pending_input=input_)

    session = scoremanager.core.Session(is_test=True)
    controllers = [
        scoremanager.core.ScoreManager(session=session, is_test=True),
        scoremanager.wranglers.ScorePackageWrangler(session=session),
        scoremanager.iotools.Menu(session=session),
        scoremanager.managers.ScorePackageManager(
            path=score_package_path,
            session=session,
            ),
        scoremanager.wranglers.SegmentPackageWrangler(session=session),
        scoremanager.managers.SegmentPackageManager(
            path=segment_package_path,
            session=session,
            ),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_08():
    r'''Stylesheet file wrangler.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score y q'
    score_manager._run(pending_input=input_)

    session = scoremanager.core.Session(is_test=True)
    controllers = [
        scoremanager.core.ScoreManager(session=session, is_test=True),
        scoremanager.wranglers.ScorePackageWrangler(session=session),
        scoremanager.iotools.Menu(session=session),
        scoremanager.managers.ScorePackageManager(
            path=score_package_path,
            session=session,
            ),
        scoremanager.wranglers.StylesheetWrangler(session=session),
        ]
    assert score_manager._session.controllers_visited == controllers