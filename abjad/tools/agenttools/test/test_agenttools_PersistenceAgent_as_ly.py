# -*- encoding: utf-8 -*-
import os
from abjad import *
configuration = systemtools.AbjadConfiguration()
ly_path = os.path.join(
    configuration.abjad_directory, 
    'test.ly',
    )
candidate_ly_path = os.path.join(
    configuration.abjad_directory,
    'test.candidate.ly',
    )


def test_agenttools_PersistenceAgent_as_ly_01():
    r'''When candidacy is true, agent persists LilyPond file when no 
    LilyPond file exists.
    '''

    note = Note("c'4")
    with systemtools.FilesystemState(remove=[ly_path, candidate_ly_path]):
        result = persist(note).as_ly(ly_path, candidacy=True)    
        assert os.path.isfile(ly_path)
        assert isinstance(result, tuple)

        
def test_agenttools_PersistenceAgent_as_ly_02():
    r'''When candidacy is true, agent refuses to persist LilyPond file when
    equivalent LilyPond file already exists.
    '''

    note = Note("c'4")
    with systemtools.FilesystemState(remove=[ly_path, candidate_ly_path]):
        result = persist(note).as_ly(ly_path)
        assert isinstance(result, tuple)
        assert os.path.isfile(ly_path)
        result = persist(note).as_ly(ly_path, candidacy=True)    
        assert result == False


def test_agenttools_PersistenceAgent_as_ly_03():
    r'''When candidacy is true, agent persists LilyPond file when
    nonequivalent LilyPond file already exists.
    '''

    note = Note("c'4")
    with systemtools.FilesystemState(remove=[ly_path, candidate_ly_path]):
        with open(ly_path, 'w') as file_pointer:
            file_pointer.write('extra text')
        with open(ly_path, 'r') as file_pointer:
            lines = file_pointer.readlines()
        contents = ''.join(lines)
        assert 'extra text' in contents
        result = persist(note).as_ly(ly_path, candidacy=True)    
        assert isinstance(result, tuple)
        assert os.path.isfile(ly_path)
        with open(ly_path, 'r') as file_pointer:
            lines = file_pointer.readlines()
        contents = ''.join(lines)
        assert 'extra text' not in contents