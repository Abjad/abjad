# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_TempoInventoryEditor___init___01():
    r'''Initializes correctly when current working directory is the score 
    manager directory.
    '''

    os.chdir(configuration.score_manager_directory_path)
    session = scoremanager.core.Session()
    editor = scoremanager.editors.TempoInventoryEditor(session=session)
    assert isinstance(editor, scoremanager.editors.TempoInventoryEditor)


def test_TempoInventoryEditor___init___02():
    r'''Initializes correctly when current working directory is a directory
    other than the score manager directory.
    '''

    os.chdir(configuration.abjad_directory_path)
    session = scoremanager.core.Session()
    editor = scoremanager.editors.TempoInventoryEditor(session=session)
    assert isinstance(editor, scoremanager.editors.TempoInventoryEditor)