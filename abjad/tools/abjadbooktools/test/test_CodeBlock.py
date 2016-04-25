# -*- coding: utf-8 -*-
import sys
import unittest
from abjad.tools import abjadbooktools
from abjad.tools import stringtools


class CodeBlockTests(unittest.TestCase):

    def test_as_docutils_01(self):
        code_block = abjadbooktools.CodeBlock(())
        code_block.output_proxies.append(
            abjadbooktools.CodeOutputProxy(
                (
                    '>>> for i in range(4):',
                    '...     print(i)',
                    '0',
                    '1',
                    '2',
                    '3',
                    '>>> 1 + 1',
                    '2',
                    ),
                ),
            )
        result = code_block.as_docutils()
        self.assertEqual(len(result), 2)
        self.assertEqual(
            stringtools.normalize(result[0].pformat()),
            stringtools.normalize(
                r'''
                <literal_block xml:space="preserve">
                    >>> for i in range(4):
                    ...     print(i)
                    0
                    1
                    2
                    3
                '''),
            )
        self.assertEqual(
            stringtools.normalize(result[1].pformat()),
            stringtools.normalize(
                r'''
                <literal_block xml:space="preserve">
                    >>> 1 + 1
                    2
                '''),
            )

    def test_from_docutils_abjad_import_block_01(self):
        source = '''
        ..  import:: abjad.tools.abjadbooktools:example_function
        '''
        source = stringtools.normalize(source)
        document = abjadbooktools.SphinxDocumentHandler.parse_rst(source)
        block = document[0]
        result = abjadbooktools.CodeBlock.from_docutils_abjad_import_block(block)
        if sys.version_info[0] == 2:
            assert format(result) == stringtools.normalize(r"""
                abjadbooktools.CodeBlock(
                    (
                        u'def example_function(expr):',
                        u"    r'''This is a multiline docstring.",
                        u'',
                        u'    This is the third line of the docstring.',
                        u"    '''",
                        u'    # This is a comment.',
                        u"    print('Entering example function.')",
                        u'    try:',
                        u'        expr = expr + 1',
                        u'    except TypeError:',
                        u"        print('Wrong type!')",
                        u'    print(expr)',
                        u"    print('Leaving example function.')",
                        ),
                    executed_lines=(
                        'from abjad.tools.abjadbooktools import example_function',
                        ),
                    starting_line_number=1,
                    )
                """)
        else:            
            assert format(result) == stringtools.normalize(r"""
                abjadbooktools.CodeBlock(
                    (
                        'def example_function(expr):',
                        "    r'''This is a multiline docstring.",
                        '',
                        '    This is the third line of the docstring.',
                        "    '''",
                        '    # This is a comment.',
                        "    print('Entering example function.')",
                        '    try:',
                        '        expr = expr + 1',
                        '    except TypeError:',
                        "        print('Wrong type!')",
                        '    print(expr)',
                        "    print('Leaving example function.')",
                        ),
                    executed_lines=(
                        'from abjad.tools.abjadbooktools import example_function',
                        ),
                    starting_line_number=1,
                    )
                """)

    def test_from_docutils_abjad_import_block_02(self):
        source = '''
        ..  import:: abjad.tools.abjadbooktools:example_function
            :hide:
        '''
        source = stringtools.normalize(source)
        document = abjadbooktools.SphinxDocumentHandler.parse_rst(source)
        block = document[0]
        result = abjadbooktools.CodeBlock.from_docutils_abjad_import_block(block)
        if sys.version_info[0] == 2:
            assert format(result) == stringtools.normalize(r"""
                abjadbooktools.CodeBlock(
                    (
                        u'def example_function(expr):',
                        u"    r'''This is a multiline docstring.",
                        u'',
                        u'    This is the third line of the docstring.',
                        u"    '''",
                        u'    # This is a comment.',
                        u"    print('Entering example function.')",
                        u'    try:',
                        u'        expr = expr + 1',
                        u'    except TypeError:',
                        u"        print('Wrong type!')",
                        u'    print(expr)',
                        u"    print('Leaving example function.')",
                        ),
                    code_block_specifier=abjadbooktools.CodeBlockSpecifier(
                        hide=True,
                        ),
                    executed_lines=(
                        'from abjad.tools.abjadbooktools import example_function',
                        ),
                    starting_line_number=1,
                    )
                """)
        else:
            assert format(result) == stringtools.normalize(r"""
                abjadbooktools.CodeBlock(
                    (
                        'def example_function(expr):',
                        "    r'''This is a multiline docstring.",
                        '',
                        '    This is the third line of the docstring.',
                        "    '''",
                        '    # This is a comment.',
                        "    print('Entering example function.')",
                        '    try:',
                        '        expr = expr + 1',
                        '    except TypeError:',
                        "        print('Wrong type!')",
                        '    print(expr)',
                        "    print('Leaving example function.')",
                        ),
                    code_block_specifier=abjadbooktools.CodeBlockSpecifier(
                        hide=True,
                        ),
                    executed_lines=(
                        'from abjad.tools.abjadbooktools import example_function',
                        ),
                    starting_line_number=1,
                    )
                """)

    def test_from_docutils_abjad_input_block_01(self):
        source = '''
        ..  abjad::

            note = Note("c'4")
            if True:
                note.written_pitch = "ds,"
        '''
        source = stringtools.normalize(source)
        document = abjadbooktools.SphinxDocumentHandler.parse_rst(source)
        block = document[0]
        result = abjadbooktools.CodeBlock.from_docutils_abjad_input_block(block)
        if sys.version_info[0] == 2:
            assert format(result) == stringtools.normalize(r"""
                abjadbooktools.CodeBlock(
                    (
                        u'note = Note("c\'4")',
                        u'if True:',
                        u'    note.written_pitch = "ds,"',
                        ),
                    starting_line_number=2,
                    )
                """)
        else:
            assert format(result) == stringtools.normalize(r"""
                abjadbooktools.CodeBlock(
                    (
                        'note = Note("c\'4")',
                        'if True:',
                        '    note.written_pitch = "ds,"',
                        ),
                    starting_line_number=2,
                    )
                """)

    def test_from_docutils_abjad_input_block_02(self):
        source = '''
        ..  abjad::
            :allow-exceptions:

            note = Note("c'4")
            if True:
                note.written_pitch = "ds,"
        '''
        source = stringtools.normalize(source)
        document = abjadbooktools.SphinxDocumentHandler.parse_rst(source)
        block = document[0]
        result = abjadbooktools.CodeBlock.from_docutils_abjad_input_block(block)
        if sys.version_info[0] == 2:
            assert format(result) == stringtools.normalize(r"""
                abjadbooktools.CodeBlock(
                    (
                        u'note = Note("c\'4")',
                        u'if True:',
                        u'    note.written_pitch = "ds,"',
                        ),
                    code_block_specifier=abjadbooktools.CodeBlockSpecifier(
                        allow_exceptions=True,
                        ),
                    starting_line_number=3,
                    )
                """)
        else:
            assert format(result) == stringtools.normalize(r"""
                abjadbooktools.CodeBlock(
                    (
                        'note = Note("c\'4")',
                        'if True:',
                        '    note.written_pitch = "ds,"',
                        ),
                    code_block_specifier=abjadbooktools.CodeBlockSpecifier(
                        allow_exceptions=True,
                        ),
                    starting_line_number=3,
                    )
                """)

    def test_from_docutils_literal_block(self):
        source = '''
        ::

            >>> print('Hello, world!')
            Hello, world!
        '''
        source = stringtools.normalize(source)
        document = abjadbooktools.SphinxDocumentHandler.parse_rst(source)
        block = document[0]
        result = abjadbooktools.CodeBlock.from_docutils_literal_block(block)
        assert result == abjadbooktools.CodeBlock(
            ("print('Hello, world!')",),
            code_block_specifier=abjadbooktools.CodeBlockSpecifier(
                allow_exceptions=True,
                ),
            starting_line_number=3,
            )
