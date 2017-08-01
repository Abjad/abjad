# -*- coding: utf-8 -*-
import os
import abjad
from abjad.tools import systemtools
configuration = systemtools.AbjadConfiguration()

path_1 = os.path.join(
    configuration.abjad_directory,
    'test_1.pdf',
    )
path_2 = os.path.join(
    configuration.abjad_directory,
    'test_2.pdf',
    )


def test_systemtools_TestManager__compare_pdfs_01():
    r'''Is true when PDFs are the same.
    '''

    with systemtools.FilesystemState(remove=[path_1]):
        note = abjad.Note("c'4")
        abjad.persist(note).as_pdf(path_1, remove_ly=True)
        assert systemtools.TestManager._compare_pdfs(path_1, path_1)


def test_systemtools_TestManager__compare_pdfs_02():
    r'''Is true when PDFs differ but contain the same music.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        note = abjad.Note("c'4")
        abjad.persist(note).as_pdf(path_1, remove_ly=True)
        note = abjad.Note("c'4")
        abjad.persist(note).as_pdf(path_2, remove_ly=True)
        assert systemtools.TestManager._compare_pdfs(path_1, path_2)


def test_systemtools_TestManager__compare_pdfs_03():
    r'''False when PDFs contain different music.
    '''

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        note = abjad.Note("c'4")
        abjad.persist(note).as_pdf(path_1, remove_ly=True)
        note = abjad.Note("d'4")
        abjad.persist(note).as_pdf(path_2, remove_ly=True)
        assert not systemtools.TestManager._compare_pdfs(path_1, path_2)
