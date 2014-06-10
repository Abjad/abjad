# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager
configuration = scoremanager.idetools.Configuration()

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
    r'''Abjad IDE.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'q'
    score_manager._run(input_=input_)

    session = scoremanager.idetools.Session(is_test=True)
    controllers = [
        scoremanager.idetools.AbjadIDE(session=session, is_test=True),
        scoremanager.idetools.ScorePackageWrangler(session=session),
        scoremanager.idetools.Menu(session=session),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_02():
    r'''Score package manager.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score q'
    score_manager._run(input_=input_)

    session = scoremanager.idetools.Session(is_test=True)
    controllers = [
        scoremanager.idetools.AbjadIDE(session=session, is_test=True),
        scoremanager.idetools.ScorePackageWrangler(session=session),
        scoremanager.idetools.Menu(session=session),
        scoremanager.idetools.ScorePackageManager(
            path=score_package_path,
            session=session,
            ),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_03():
    r'''Build file wrangler.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score u q'
    score_manager._run(input_=input_)

    session = scoremanager.idetools.Session(is_test=True)
    controllers = [
        scoremanager.idetools.AbjadIDE(session=session, is_test=True),
        scoremanager.idetools.ScorePackageWrangler(session=session),
        scoremanager.idetools.Menu(session=session),
        scoremanager.idetools.ScorePackageManager(
            session=session,
            path=score_package_path,
            ),
        scoremanager.idetools.BuildFileWrangler(session=session),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_04():
    r'''Material package manager.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m q'
    score_manager._run(input_=input_)

    session = scoremanager.idetools.Session(is_test=True)
    controllers = [
        scoremanager.idetools.AbjadIDE(session=session, is_test=True),
        scoremanager.idetools.ScorePackageWrangler(session=session),
        scoremanager.idetools.Menu(session=session),
        scoremanager.idetools.ScorePackageManager(
            path=score_package_path,
            session=session,
            ),
        scoremanager.idetools.MaterialPackageWrangler(session=session),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_05():
    r'''Material package manager.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m tempo~inventory q'
    score_manager._run(input_=input_)

    session = scoremanager.idetools.Session(is_test=True)
    controllers = [
        scoremanager.idetools.AbjadIDE(session=session, is_test=True),
        scoremanager.idetools.ScorePackageWrangler(session=session),
        scoremanager.idetools.Menu(session=session),
        scoremanager.idetools.ScorePackageManager(
            path=score_package_path,
            session=session,
            ),
        scoremanager.idetools.MaterialPackageWrangler(session=session),
        scoremanager.idetools.MaterialPackageManager(
            path=tempo_inventory_package_path,
            session=session,
            ),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_06():
    r'''Segment wrangler.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g q'
    score_manager._run(input_=input_)

    session = scoremanager.idetools.Session(is_test=True)
    controllers = [
        scoremanager.idetools.AbjadIDE(session=session, is_test=True),
        scoremanager.idetools.ScorePackageWrangler(session=session),
        scoremanager.idetools.Menu(session=session),
        scoremanager.idetools.ScorePackageManager(
            path=score_package_path,
            session=session,
            ),
        scoremanager.idetools.SegmentPackageWrangler(session=session),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_07():
    r'''Segment package manager.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g 1 q'
    score_manager._run(input_=input_)

    session = scoremanager.idetools.Session(is_test=True)
    controllers = [
        scoremanager.idetools.AbjadIDE(session=session, is_test=True),
        scoremanager.idetools.ScorePackageWrangler(session=session),
        scoremanager.idetools.Menu(session=session),
        scoremanager.idetools.ScorePackageManager(
            path=score_package_path,
            session=session,
            ),
        scoremanager.idetools.SegmentPackageWrangler(session=session),
        scoremanager.idetools.SegmentPackageManager(
            path=segment_package_path,
            session=session,
            ),
        ]
    assert score_manager._session.controllers_visited == controllers


def test_Session_controllers_visited_08():
    r'''Stylesheet file wrangler.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score y q'
    score_manager._run(input_=input_)

    session = scoremanager.idetools.Session(is_test=True)
    controllers = [
        scoremanager.idetools.AbjadIDE(session=session, is_test=True),
        scoremanager.idetools.ScorePackageWrangler(session=session),
        scoremanager.idetools.Menu(session=session),
        scoremanager.idetools.ScorePackageManager(
            path=score_package_path,
            session=session,
            ),
        scoremanager.idetools.StylesheetWrangler(session=session),
        ]
    assert score_manager._session.controllers_visited == controllers