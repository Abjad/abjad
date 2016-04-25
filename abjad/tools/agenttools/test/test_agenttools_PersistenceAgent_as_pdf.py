# -*- coding: utf-8 -*-
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
paths = [ly_path, pdf_path]


def test_agenttools_PersistenceAgent_as_pdf_01():
    r'''Agent persists PDF file when no PDF file exists.
    '''

    note = Note("c'4")
    with systemtools.FilesystemState(remove=paths):
        result = persist(note).as_pdf(pdf_path)
        assert os.path.isfile(pdf_path)
        assert isinstance(result, tuple)


def test_agenttools_PersistenceAgent_as_pdf_02():
    r'''Agent persists PDF file when equivalent PDF file already exists.
    '''

    note = Note("c'4")
    with systemtools.FilesystemState(remove=paths):
        result = persist(note).as_pdf(pdf_path)
        assert os.path.isfile(pdf_path)
        assert isinstance(result, tuple)
        os.remove(ly_path)
        persist(note).as_pdf(pdf_path)
        assert os.path.isfile(pdf_path)
