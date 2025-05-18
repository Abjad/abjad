import os

import abjad

configuration = abjad.Configuration()
ly_path = configuration.abjad_directory / "test.ly"
pdf_path = configuration.abjad_directory / "test.pdf"
png_path = configuration.abjad_directory / "test.png"
png_preview_path = configuration.abjad_directory / "test.preview.png"
paths = [ly_path, pdf_path, png_path, png_preview_path]


def test_persist_as_ly_01():
    """
    Persists LilyPond file when no LilyPond file exists.
    """

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=[ly_path]):
        result = abjad.persist.as_ly(note, ly_path)
        assert os.path.isfile(ly_path)
        assert isinstance(result, tuple)


def test_persist_as_ly_02():
    """
    Persists LilyPond file when LilyPond file already exists.
    """

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=[ly_path]):
        result = abjad.persist.as_ly(note, ly_path)
        assert isinstance(result, tuple)
        assert os.path.isfile(ly_path)
        abjad.persist.as_ly(note, ly_path)
        assert os.path.isfile(ly_path)


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


def test_persist_as_png_01():
    """
    Persist PNG.
    """

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=paths):
        result = abjad.persist.as_png(note, png_path)
        assert os.path.isfile(png_path)
        assert isinstance(result, tuple)
        os.remove(ly_path)
        abjad.persist.as_png(note, png_path)
        assert os.path.isfile(png_path)


def test_persist_as_png_02():
    """
    Persist PNG with preview.
    """

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=paths):
        result = abjad.persist.as_png(note, png_path, preview=True)
        assert os.path.isfile(png_path)
        assert os.path.isfile(png_preview_path)
        assert isinstance(result, tuple)
        os.remove(ly_path)
        abjad.persist.as_png(note, png_path, preview=True)
        assert os.path.isfile(png_path)
        assert os.path.isfile(png_preview_path)
