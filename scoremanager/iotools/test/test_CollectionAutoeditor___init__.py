# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.Configuration()


def test_CollectionAutoeditor___init___01():
    r'''Initializes correctly when current working directory is the score
    manager directory.
    '''

    os.chdir(configuration.score_manager_directory)
    session = scoremanager.core.Session()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(session=session)
    assert isinstance(autoeditor, scoremanager.iotools.CollectionAutoeditor)


def test_CollectionAutoeditor___init___02():
    r'''Initializes correctly when current working directory is a directory
    other than the score manager directory.
    '''

    os.chdir(configuration.abjad_directory)
    session = scoremanager.core.Session()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(session=session)
    assert isinstance(autoeditor, scoremanager.iotools.CollectionAutoeditor)