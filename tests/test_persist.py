import os

import pytest

import abjad

configuration = abjad.Configuration()
ly_path = configuration.abjad_directory / "test.ly"
midi_path = configuration.abjad_directory / "test.midi"
pdf_path = configuration.abjad_directory / "test.pdf"
png_path = configuration.abjad_directory / "test.png"
paths = [ly_path, midi_path, pdf_path, png_path]


def test_persist_as_ly_01():
    """
    Persists LilyPond file when no LilyPond file exists.
    """

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=[ly_path]):
        abjad_format_time = abjad.persist.as_ly(note, ly_path)
        assert os.path.isfile(ly_path)
        assert isinstance(abjad_format_time, float)


def test_persist_as_ly_02():
    """
    Persists LilyPond file when LilyPond file already exists.
    """

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=[ly_path]):
        abjad_format_time = abjad.persist.as_ly(note, ly_path)
        assert isinstance(abjad_format_time, float)
        assert os.path.isfile(ly_path)
        abjad.persist.as_ly(note, ly_path)
        assert os.path.isfile(ly_path)


@pytest.mark.skip("refactor MIDI persistence")
def test_persist_as_midi_01():
    """
    Persists MIDI file when no MIDI file exists.
    """

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=paths):
        result = abjad.persist.as_midi(note, midi_path)
        assert os.path.isfile(midi_path)
        assert isinstance(result, tuple)


@pytest.mark.skip("refactor MIDI persistence")
def test_persist_as_midi_02():
    """
    Persists MIDI file when equivalent MIDI file already exists.
    """

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=paths):
        result = abjad.persist.as_midi(note, midi_path)
        assert os.path.isfile(midi_path)
        assert isinstance(result, tuple)
        os.remove(ly_path)
        abjad.persist.as_midi(note, midi_path)
        assert os.path.isfile(midi_path)


def test_persist_as_pdf_01():
    """
    Persists PDF when no PDF exists.
    """

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=paths):
        result = abjad.persist.as_pdf(note, pdf_path)
        assert os.path.isfile(pdf_path)
        assert isinstance(result, tuple)


def test_persist_as_pdf_02():
    """
    Persists PDF when equivalent PDF already exists.
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
    Persists PNG when no PNG exists.
    """

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=paths):
        result = abjad.persist.as_png(note, png_path)
        assert os.path.isfile(png_path)
        assert isinstance(result, tuple)


def test_persist_as_png_02():
    """
    Persists PNG when equivalent PNG already exists.
    """

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=paths):
        result = abjad.persist.as_png(note, png_path)
        assert os.path.isfile(png_path)
        assert isinstance(result, tuple)
        os.remove(ly_path)
        abjad.persist.as_png(note, png_path)
        assert os.path.isfile(png_path)
