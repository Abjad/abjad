# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_ListAutoeditor___init___01():
    r'''Initializes correctly when current working directory is the score
    manager directory.
    '''

    os.chdir(configuration.score_manager_directory)
    session = scoremanager.core.Session()
    autoeditor = scoremanager.iotools.ListAutoeditor(session=session)
    assert isinstance(autoeditor, scoremanager.iotools.ListAutoeditor)


def test_ListAutoeditor___init___02():
    r'''Initializes correctly when current working directory is a directory
    other than the score manager directory.
    '''

    os.chdir(configuration.abjad_directory)
    session = scoremanager.core.Session()
    autoeditor = scoremanager.iotools.ListAutoeditor(session=session)
    assert isinstance(autoeditor, scoremanager.iotools.ListAutoeditor)