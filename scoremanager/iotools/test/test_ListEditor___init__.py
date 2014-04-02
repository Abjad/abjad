# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_ListEditor___init___01():
    r'''Initializes correctly when current working directory is the score 
    manager directory.
    '''

    os.chdir(configuration.score_manager_directory_path)
    session = scoremanager.core.Session()
    editor = scoremanager.iotools.ListEditor(session=session)
    assert isinstance(editor, scoremanager.iotools.ListEditor)


def test_ListEditor___init___02():
    r'''Initializes correctly when current working directory is a directory
    other than the score manager directory.
    '''

    os.chdir(configuration.abjad_directory_path)
    session = scoremanager.core.Session()
    editor = scoremanager.iotools.ListEditor(session=session)
    assert isinstance(editor, scoremanager.iotools.ListEditor)