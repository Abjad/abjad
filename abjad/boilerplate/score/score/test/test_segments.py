import abjad
import difflib
import ide
import os
import pathlib
import pytest
import shutil
import sys


abjad_ide = ide.AbjadIDE()
scores = pathlib.Path(*pathlib.Path(__file__).parts[:-4])
path = ide.Path(__file__, scores=scores)
directories = path.segments.list_paths()


@pytest.mark.parametrize('directory', directories)
def test_segments_01(directory):
    exit_code = abjad_ide.check_definition_py(directory)
    if exit_code != 0:
        sys.exit(exit_code)


@pytest.mark.parametrize('directory', directories)
def test_segments_02(directory):
    # only run on Travis because segment illustration usually takes a while
    if not os.getenv('TRAVIS'):
        return
    with abjad.FilesystemState(keep=[directory]):
        ly = directory / 'illustration.ly'
        ly_old = directory / 'illustration.old.ly'
        if ly.exists():
            shutil.copyfile(ly, ly_old)
        exit_code = abjad_ide.make_illustration_pdf(
            directory,
            open_after=False,
            )
        if exit_code != 0:
            sys.exit(exit_code)
        if not ly_old.exists():
            return
        assert ly.exists()
        assert ly_old.exists()
        if not abjad.TestManager.compare_files(ly_old, ly):
            ly_old_text = ly_old.read_text().splitlines(keepends=True)
            ly_text = ly.read_text().splitlines(keepends=True)
            print(''.join(difflib.ndiff(ly_old_text, ly_text)))
            sys.exit(1)
