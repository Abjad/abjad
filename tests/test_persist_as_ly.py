import os

import abjad

configuration = abjad.Configuration()
ly_path = configuration.abjad_directory / "test.ly"


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
