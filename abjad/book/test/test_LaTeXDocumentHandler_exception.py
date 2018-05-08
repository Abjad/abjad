import pytest
import abjad.book
from uqbar.strings import normalize


def test_exception_1():
    input_file_contents = [
        '<abjad>',
        "'foo' / 19",
        '</abjad>',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    with pytest.raises(abjad.book.AbjadBookError):
        document_handler(return_source=True)


def test_exception_2():
    input_file_contents = [
        '<abjad>[allow_exceptions=true]',
        "'foo' / 19",
        '</abjad>',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    rebuilt_source = document_handler(return_source=True)
    assert rebuilt_source == normalize(
        '''
        <abjad>[allow_exceptions=true]
        'foo' / 19
        </abjad>

        %%% ABJADBOOK START %%%
        \\begin{lstlisting}
        >>> 'foo' / 19
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        TypeError: unsupported operand type(s) for /: 'str' and 'int'
        \\end{lstlisting}
        %%% ABJADBOOK END %%%
        ''',
        )


def test_exception_3():
    input_file_contents = [
        '<abjad>[allow_exceptions=true]',
        "'foo' / 19",
        '</abjad>',
        '',
        '<abjad>',
        "23 + 'baz'",
        '</abjad>',
        ]
    document_handler = abjad.book.LaTeXDocumentHandler(
        input_file_contents=input_file_contents,
        )
    with pytest.raises(abjad.book.AbjadBookError):
        document_handler(return_source=True)
