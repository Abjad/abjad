import ide
import pathlib
import pytest
import sys


abjad_ide = ide.AbjadIDE()
scores = pathlib.Path(*pathlib.Path(__file__).parts[:-4])
path = ide.Path(__file__, scores=scores)
directories = path.materials.list_paths()


@pytest.mark.parametrize('directory', directories)
def test_materials_01(directory):
    exit_code = abjad_ide.check_definition_py(directory)
    if exit_code != 0:
        sys.exit(exit_code)


@pytest.mark.parametrize('directory', directories)
def test_materials_02(directory):
    exit_code = abjad_ide.make_illustration_pdf(directory, open_after=False)
    if exit_code != 0:
        sys.exit(exit_code)
