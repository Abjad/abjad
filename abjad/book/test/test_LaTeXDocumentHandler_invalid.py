import pytest
import abjad.book


def test_invalid_source_1():
    input_file_contents = [
        '<abjad>',
        '<abjad>',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    with pytest.raises(ValueError):
        document_handler(return_source=True)


def test_invalid_source_2():
    input_file_contents = [
        '<abjad>',
        '%%% ABJADBOOK START %%%',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    with pytest.raises(ValueError):
        document_handler(return_source=True)


def test_invalid_source_3():
    input_file_contents = [
        '<abjad>',
        '%%% ABJADBOOK END %%%',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    with pytest.raises(ValueError):
        document_handler(return_source=True)


def test_invalid_source_4():
    input_file_contents = [
        '%%% ABJADBOOK START %%%',
        '%%% ABJADBOOK START %%%',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    with pytest.raises(ValueError):
        document_handler(return_source=True)


def test_invalid_source_5():
    input_file_contents = [
        '%%% ABJADBOOK START %%%',
        '<abjad>',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    with pytest.raises(ValueError):
        document_handler(return_source=True)


def test_invalid_source_6():
    input_file_contents = [
        '%%% ABJADBOOK START %%%',
        '</abjad>',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    with pytest.raises(ValueError):
        document_handler(return_source=True)


def test_invalid_source_7():
    input_file_contents = [
        ''
        '</abjad>',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    with pytest.raises(ValueError):
        document_handler(return_source=True)


def test_invalid_source_8():
    input_file_contents = [
        ''
        '%%% ABJADBOOK END %%%',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    with pytest.raises(ValueError):
        document_handler(return_source=True)
