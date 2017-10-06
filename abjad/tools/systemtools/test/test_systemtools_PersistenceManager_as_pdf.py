import abjad
import os
configuration = abjad.AbjadConfiguration()
ly_path = os.path.join(
    configuration.abjad_directory,
    'test.ly',
    )
pdf_path = os.path.join(
    configuration.abjad_directory,
    'test.pdf',
    )
paths = [ly_path, pdf_path]


def test_systemtools_PersistenceManager_as_pdf_01():
    r'''Agent abjad.persists PDF file when no PDF file exists.
    '''

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=paths):
        result = abjad.persist(note).as_pdf(pdf_path)
        assert os.path.isfile(pdf_path)
        assert isinstance(result, tuple)


def test_systemtools_PersistenceManager_as_pdf_02():
    r'''Agent abjad.persists PDF file when equivalent PDF file already exists.
    '''

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=paths):
        result = abjad.persist(note).as_pdf(pdf_path)
        assert os.path.isfile(pdf_path)
        assert isinstance(result, tuple)
        os.remove(ly_path)
        abjad.persist(note).as_pdf(pdf_path)
        assert os.path.isfile(pdf_path)
