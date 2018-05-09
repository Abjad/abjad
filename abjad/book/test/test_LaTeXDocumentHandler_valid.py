import abjad.book
import os
import pytest
import shutil


test_directory = os.path.dirname(__file__)
assets_directory = os.path.join(test_directory, 'assets')
source_valid_path = os.path.join(test_directory, 'source_valid.tex')
with open(source_valid_path, 'r') as file_pointer:
    source_valid_contents = file_pointer.read().rstrip()
target_valid_path = os.path.join(test_directory, 'target_valid.tex')

expected_valid_path = os.path.join(test_directory, 'expected_valid.tex')
with open(expected_valid_path, 'r') as file_pointer:
    expected_valid_contents = file_pointer.read().rstrip()
expected_asset_names = tuple(sorted([
    'graphviz-a20bf977ab8d78c92f80a64305ccbe7b.dot',
    'graphviz-a20bf977ab8d78c92f80a64305ccbe7b.pdf',
    'lilypond-083d0fee82447554abe774beecddec5d.ly',
    'lilypond-083d0fee82447554abe774beecddec5d.pdf',
    'lilypond-4296e8f4e63a8d4646a441f14ec2cbf1.ly',
    'lilypond-4296e8f4e63a8d4646a441f14ec2cbf1.pdf',
    'lilypond-5af429d4d8ec9363c325eb63be7fd97f.ly',
    'lilypond-5af429d4d8ec9363c325eb63be7fd97f.pdf',
    'lilypond-c2c99b4946903c7f3d324af1a82a52f3.ly',
    'lilypond-c2c99b4946903c7f3d324af1a82a52f3.pdf',
    'lilypond-d3ecbde01b2f252633e28953dae06eea.ly',
    'lilypond-d3ecbde01b2f252633e28953dae06eea.pdf',
    ]))

stylesheet_path = os.path.join(test_directory, 'stylesheet.ily')
expected_styled_path = os.path.join(test_directory, 'expected_styled.tex')
with open(expected_styled_path, 'r') as file_pointer:
    expected_styled_contents = file_pointer.read().rstrip()
styled_asset_names = tuple(sorted([
    'graphviz-a20bf977ab8d78c92f80a64305ccbe7b.dot',
    'graphviz-a20bf977ab8d78c92f80a64305ccbe7b.pdf',
    'lilypond-14463b9f591e108d75c484d50a774bcf.ly',
    'lilypond-14463b9f591e108d75c484d50a774bcf.pdf',
    'lilypond-4046a5a421974373bc0ce276292d197a.ly',
    'lilypond-4046a5a421974373bc0ce276292d197a.pdf',
    'lilypond-810787b0fbb6aaebefda585b48682ab4.ly',
    'lilypond-810787b0fbb6aaebefda585b48682ab4.pdf',
    'lilypond-9525588d8fad504c34201efaf3bb5f18.ly',
    'lilypond-9525588d8fad504c34201efaf3bb5f18.pdf',
    'lilypond-eb26c8d836ad790ef3f3c19b5dbd0885.ly',
    'lilypond-eb26c8d836ad790ef3f3c19b5dbd0885.pdf',
    ]))

configuration_path = os.path.join(test_directory, 'configuration.cfg')
expected_configured_path = os.path.join(
    test_directory, 'expected_configured.tex')
with open(expected_configured_path, 'r') as file_pointer:
    expected_configured_contents = file_pointer.read().rstrip()


@pytest.fixture
def paths():
    if os.path.exists(assets_directory):
        shutil.rmtree(assets_directory)
    if os.path.exists(target_valid_path):
        os.remove(target_valid_path)
    yield
    if os.path.exists(assets_directory):
        shutil.rmtree(assets_directory)
    if os.path.exists(target_valid_path):
        os.remove(target_valid_path)
    with open(source_valid_path, 'w') as file_pointer:
        file_pointer.write(source_valid_contents)


def test_clean(paths):
    document_handler = abjad.book.LaTeXDocumentHandler.from_path(
        input_file_path=source_valid_path)
    document_handler()
    with open(source_valid_path, 'r') as file_pointer:
        target_valid_contents = file_pointer.read()
    assert abjad.String.normalize(str(target_valid_contents)) == \
        abjad.String.normalize(str(expected_valid_contents))
    document_handler = abjad.book.LaTeXDocumentHandler.from_path(
        input_file_path=source_valid_path)
    document_handler(clean=True)
    with open(source_valid_path, 'r') as file_pointer:
        target_valid_contents = file_pointer.read()
    assert target_valid_contents == source_valid_contents


def test_configured(paths):
    configuration = abjad.book.AbjadBookScript()._read_config(
        configuration_path)
    assert not os.path.exists(target_valid_path)
    assert not os.path.exists(assets_directory)
    document_handler = abjad.book.LaTeXDocumentHandler.from_path(
        input_file_path=source_valid_path)
    document_handler(
        configuration=configuration,
        output_file_path=target_valid_path,
        )
    assert os.path.exists(target_valid_path)
    assert os.path.exists(assets_directory)
    with open(target_valid_path, 'r') as file_pointer:
        target_valid_contents = file_pointer.read()
    assert target_valid_contents == expected_configured_contents
    assert tuple(sorted(os.listdir(assets_directory))) == \
        expected_asset_names


def test_double_source(paths):
    assert not os.path.exists(target_valid_path)
    assert not os.path.exists(assets_directory)
    document_handler = abjad.book.LaTeXDocumentHandler.from_path(
        input_file_path=source_valid_path)
    document_handler(output_file_path=target_valid_path)
    assert os.path.exists(target_valid_path)
    assert os.path.exists(assets_directory)
    with open(target_valid_path, 'r') as file_pointer:
        target_valid_contents = file_pointer.read()
    assert target_valid_contents == expected_valid_contents
    assert tuple(sorted(os.listdir(assets_directory))) == \
        expected_asset_names


def test_return_source(paths):
    assert not os.path.exists(assets_directory)
    document_handler = abjad.book.LaTeXDocumentHandler.from_path(
        input_file_path=source_valid_path)
    target_valid_contents = document_handler(return_source=True)
    assert target_valid_contents == expected_valid_contents


def test_single_source(paths):
    assert not os.path.exists(assets_directory)
    document_handler = abjad.book.LaTeXDocumentHandler.from_path(
        input_file_path=source_valid_path)
    document_handler()
    assert os.path.exists(source_valid_path)
    assert os.path.exists(assets_directory)
    with open(source_valid_path, 'r') as file_pointer:
        target_valid_contents = file_pointer.read()
    assert target_valid_contents == expected_valid_contents
    assert tuple(sorted(os.listdir(assets_directory))) == \
        expected_asset_names


def test_single_source_rebuild(paths):
    assert not os.path.exists(assets_directory)
    document_handler = abjad.book.LaTeXDocumentHandler.from_path(
        input_file_path=source_valid_path)
    document_handler()
    assert os.path.exists(source_valid_path)
    assert os.path.exists(assets_directory)
    with open(source_valid_path, 'r') as file_pointer:
        target_valid_contents = file_pointer.read()
    assert target_valid_contents == expected_valid_contents
    assert tuple(sorted(os.listdir(assets_directory))) == \
        expected_asset_names
    document_handler = abjad.book.LaTeXDocumentHandler.from_path(
        input_file_path=source_valid_path)
    document_handler()
    assert os.path.exists(source_valid_path)
    assert os.path.exists(assets_directory)
    with open(source_valid_path, 'r') as file_pointer:
        target_valid_contents = file_pointer.read()
    assert target_valid_contents == expected_valid_contents
    assert tuple(sorted(os.listdir(assets_directory))) == \
        expected_asset_names


def test_skip_rendering(paths):
    assert not os.path.exists(target_valid_path)
    assert not os.path.exists(assets_directory)
    document_handler = abjad.book.LaTeXDocumentHandler.from_path(
        input_file_path=source_valid_path)
    document_handler(
        output_file_path=target_valid_path,
        skip_rendering=True,
        )
    assert os.path.exists(target_valid_path)
    assert not os.path.exists(assets_directory)
    with open(target_valid_path, 'r') as file_pointer:
        target_valid_contents = file_pointer.read()
    assert target_valid_contents == expected_valid_contents


def test_stylesheet(paths):
    assert not os.path.exists(target_valid_path)
    assert not os.path.exists(assets_directory)
    document_handler = abjad.book.LaTeXDocumentHandler.from_path(
        input_file_path=source_valid_path)
    document_handler(
        output_file_path=target_valid_path,
        stylesheet=stylesheet_path,
        )
    assert os.path.exists(target_valid_path)
    assert os.path.exists(assets_directory)
    with open(target_valid_path, 'r') as file_pointer:
        target_valid_contents = file_pointer.read()
    assert target_valid_contents == expected_styled_contents
    assert tuple(sorted(os.listdir(assets_directory))) == \
        styled_asset_names
