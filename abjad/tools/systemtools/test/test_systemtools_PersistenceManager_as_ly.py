import abjad
import os
configuration = abjad.AbjadConfiguration()
ly_path = os.path.join(
    configuration.abjad_directory, 
    'test.ly',
    )


def test_systemtools_PersistenceManager_as_ly_01():
    r'''Agent abjad.persists LilyPond file when no LilyPond file exists.
    '''

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=[ly_path]):
        result = abjad.persist(note).as_ly(ly_path)
        assert os.path.isfile(ly_path)
        assert isinstance(result, tuple)

        
def test_systemtools_PersistenceManager_as_ly_02():
    r'''Agent abjad.persists LilyPond file when LilyPond file already exists.
    '''

    note = abjad.Note("c'4")
    with abjad.FilesystemState(remove=[ly_path]):
        result = abjad.persist(note).as_ly(ly_path)
        assert isinstance(result, tuple)
        assert os.path.isfile(ly_path)
        abjad.persist(note).as_ly(ly_path)
        assert os.path.isfile(ly_path)
