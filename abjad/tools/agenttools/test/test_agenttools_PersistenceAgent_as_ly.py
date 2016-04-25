# -*- coding: utf-8 -*-
import os
from abjad import *
configuration = systemtools.AbjadConfiguration()
ly_path = os.path.join(
    configuration.abjad_directory, 
    'test.ly',
    )


def test_agenttools_PersistenceAgent_as_ly_01():
    r'''Agent persists LilyPond file when no LilyPond file exists.
    '''

    note = Note("c'4")
    with systemtools.FilesystemState(remove=[ly_path]):
        result = persist(note).as_ly(ly_path)
        assert os.path.isfile(ly_path)
        assert isinstance(result, tuple)

        
def test_agenttools_PersistenceAgent_as_ly_02():
    r'''Agent persists LilyPond file when LilyPond file already exists.
    '''

    note = Note("c'4")
    with systemtools.FilesystemState(remove=[ly_path]):
        result = persist(note).as_ly(ly_path)
        assert isinstance(result, tuple)
        assert os.path.isfile(ly_path)
        persist(note).as_ly(ly_path)
        assert os.path.isfile(ly_path)
