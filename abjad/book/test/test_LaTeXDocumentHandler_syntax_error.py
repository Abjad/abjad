import pytest
import abjad.book


def test_syntax_error_1():
    input_file_contents = [
        '<abjad>',
        'foo bar baz',
        '</abjad>',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    with pytest.raises(abjad.book.AbjadBookError):
        document_handler()


def test_syntax_error_2():
    input_file_contents = [
        '<abjad>[allow_exceptions=true]',
        'foo bar baz',
        '</abjad>',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    rebuilt_source = document_handler(return_source=True)
    assert rebuilt_source == abjad.String.normalize(
        '''
        <abjad>[allow_exceptions=true]
        foo bar baz
        </abjad>

        %%% ABJADBOOK START %%%
        \\begin{lstlisting}
        >>> foo bar baz
          File "<stdin>", line 1
            foo bar baz
                  ^
        SyntaxError: invalid syntax
        \\end{lstlisting}
        %%% ABJADBOOK END %%%
        ''',
        )


def test_syntax_error_3():
    input_file_contents = [
        '<abjad>[allow_exceptions=true]',
        'foo bar baz',
        '</abjad>',
        '',
        '<abjad>',
        'foo bar baz',
        '</abjad>',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    with pytest.raises(abjad.book.AbjadBookError):
        document_handler()
