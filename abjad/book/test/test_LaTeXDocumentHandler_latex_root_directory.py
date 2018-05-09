import abjad.book
import os
import pytest
import shutil
from uqbar.strings import normalize


test_directory = os.path.dirname(__file__)
assets_directory = os.path.join(test_directory, 'assets')
source_path = os.path.join(
    test_directory,
    'chapters',
    'chapter-1',
    'source.tex',
    )

with open(source_path, 'r') as file_pointer:
    source_contents = file_pointer.read()
target_path = os.path.join(
    test_directory,
    'chapters',
    'chapter-1',
    'target.tex',
    )
expected_path = os.path.join(
    test_directory,
    'chapters',
    'chapter-1',
    'expected.tex',
    )

with open(expected_path, 'r') as file_pointer:
    expected_contents = file_pointer.read()
expected_asset_names = (
    'lilypond-5af429d4d8ec9363c325eb63be7fd97f.ly',
    'lilypond-5af429d4d8ec9363c325eb63be7fd97f.pdf',
    )


@pytest.fixture
def paths():
    if os.path.exists(assets_directory):
        shutil.rmtree(assets_directory)
    if os.path.exists(target_path):
        os.remove(target_path)
    yield
    if os.path.exists(assets_directory):
        shutil.rmtree(assets_directory)
    if os.path.exists(target_path):
        os.remove(target_path)
    with open(source_path, 'w') as file_pointer:
        file_pointer.write(source_contents)


def test_latex_root_directory_1(paths):
    input_file_contents = [
        '\\begin{comment}',
        '<abjad>',
        'note = Note(0, (1, 4))',
        'abjad.show(note)',
        '</abjad>',
        '\\end{comment}',
        ]
    assets_directory = 'ExamplePaper/assets'
    input_file_path = 'ExamplePaper/chapters/chapter-1/section-2.tex'
    latex_root_directory = 'ExamplePaper'
    document_handler = abjad.book.LaTeXDocumentHandler(
        assets_directory=assets_directory,
        input_file_contents=input_file_contents,
        input_file_path=input_file_path,
        latex_root_directory=latex_root_directory,
        )
    rebuilt_source = document_handler(return_source=True)
    assert rebuilt_source == normalize(
        '''
        \\begin{comment}
        <abjad>
        note = Note(0, (1, 4))
        abjad.show(note)
        </abjad>
        \\end{comment}

        %%% ABJADBOOK START %%%
        \\begin{lstlisting}
        >>> note = Note(0, (1, 4))
        >>> abjad.show(note)
        \\end{lstlisting}
        \\noindent\\includegraphics{assets/lilypond-5af429d4d8ec9363c325eb63be7fd97f.pdf}
        %%% ABJADBOOK END %%%
        ''',
        )


def test_latex_root_directory_2(paths):
    assert not os.path.exists(target_path)
    assert not os.path.exists(assets_directory)
    document_handler = abjad.book.LaTeXDocumentHandler.from_path(
        input_file_path=source_path,
        assets_directory=assets_directory,
        latex_root_directory=test_directory,
        )
    document_handler(output_file_path=target_path)
    assert os.path.exists(target_path)
    assert os.path.exists(assets_directory)
    with open(target_path, 'r') as file_pointer:
        target_contents = file_pointer.read()
    assert normalize(target_contents) == \
        normalize(expected_contents)
    assert tuple(sorted(os.listdir(assets_directory))) == \
        expected_asset_names
