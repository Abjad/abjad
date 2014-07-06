# -*- encoding: utf-8 -*-
import os
from abjad import *
configuration = systemtools.AbjadConfiguration()
ly_path = os.path.join(
    configuration.abjad_directory,
    'test.ly',
    )
pdf_path = os.path.join(
    configuration.abjad_directory,
    'test.pdf',
    )
candidate_pdf_path = os.path.join(
    configuration.abjad_directory,
    'test.candidate.pdf',
    )
paths = [ly_path, pdf_path, candidate_pdf_path]


def test_agenttools_PersistenceAgent_as_pdf_01():
    r'''When candidacy is true, agent persists PDF file when no
    PDF file exists.
    '''

    note = Note("c'4")
    with systemtools.FilesystemState(remove=paths):
        result = persist(note).as_pdf(pdf_path, candidacy=True)
        assert os.path.isfile(pdf_path)
        assert isinstance(result, tuple)


def test_agenttools_PersistenceAgent_as_pdf_02():
    r'''When candidacy is true, agent refuses to persist PDF file when
    equivalent PDF file already exists.
    '''

    note = Note("c'4")
    with systemtools.FilesystemState(remove=paths):
        result = persist(note).as_pdf(pdf_path, candidacy=True)
        assert os.path.isfile(pdf_path)
        assert isinstance(result, tuple)
        os.remove(ly_path)
        result = persist(note).as_pdf(pdf_path, candidacy=True)
        assert result == False


def test_agenttools_PersistenceAgent_as_pdf_03():
    r'''When candidacy is true, agent persists PDF file when
    nonequivalent PDF file already exists.
    '''

    note = Note("c'4")
    with systemtools.FilesystemState(remove=paths):
        with open(pdf_path, 'w') as file_pointer:
            file_pointer.write('extra text')
        with open(pdf_path, 'r') as file_pointer:
            lines = file_pointer.readlines()
        contents = ''.join(lines)
        assert 'extra text' in contents
        result = persist(note).as_pdf(pdf_path, candidacy=True)
        assert isinstance(result, tuple)
        with open(pdf_path, 'rb') as file_pointer:
            lines = file_pointer.readlines()
        contents = b''.join(lines)
        assert b'extra text' not in contents
