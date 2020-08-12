import os

import abjad

configuration = abjad.Configuration()
ly_path = configuration.abjad_directory / "test.ly"
pdf_path = configuration.abjad_directory / "test.pdf"
paths = [ly_path, pdf_path]


def test_persist_as_pdf_01():
    """
    Persists PDF file when no PDF file exists.
    """

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=paths):
        result = abjad.persist.as_pdf(note, pdf_path)
        assert os.path.isfile(pdf_path)
        assert isinstance(result, tuple)


def test_persist_as_pdf_02():
    """
    Persists PDF file when equivalent PDF file already exists.
    """

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=paths):
        result = abjad.persist.as_pdf(note, pdf_path)
        assert os.path.isfile(pdf_path)
        assert isinstance(result, tuple)
        os.remove(ly_path)
        abjad.persist.as_pdf(note, pdf_path)
        assert os.path.isfile(pdf_path)
