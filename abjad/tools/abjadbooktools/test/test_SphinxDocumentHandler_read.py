# -*- coding: utf-8 -*-
import platform
import unittest
from abjad.tools import abjadbooktools
from abjad.tools import stringtools
from abjad.tools import systemtools


@unittest.skipIf(
    platform.python_implementation() != 'CPython',
    'Only for CPython.',
    )
class SphinxDocumentHandlerTests(unittest.TestCase):

    class Namespace(object):
        pass

    source_one = r'''
    ..  abjad::
        :hide:

        from abjad import *

    ::

        >>> string = 'Hello, world!'

    ..  import:: abjad.tools.abjadbooktools:example_function

    ::

        >>> print(string)
        Hello, world!

    ..  abjad::

        example_function(23)
    '''
    source_one = stringtools.normalize(source_one)

    def setUp(self):
        app = self.Namespace()
        config = self.Namespace()
        self.app = app
        self.app.config = config
        self.app.config.abjadbook_ignored_documents = ()

    def test_collect_abjad_input_blocks_01(self):
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(self.source_one)
        blocks = handler.collect_abjad_input_blocks(document)
        assert len(blocks) == 3
        nodes = tuple(blocks.keys())
        assert nodes[0] is document[0]
        assert nodes[1] is document[2]
        assert nodes[2] is document[4]

    def test_collect_python_literal_blocks_01(self):
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(self.source_one)
        blocks = handler.collect_python_literal_blocks(
            document,
            renderable_only=False,
            )
        assert len(blocks) == 2
        nodes = tuple(blocks.keys())
        assert nodes[0] is document[1]
        assert nodes[1] is document[3]

    def test_collect_python_literal_blocks_02(self):
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(self.source_one)
        blocks = handler.collect_python_literal_blocks(document)
        assert len(blocks) == 0

    def test_on_doctree_read_01(self):
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(self.source_one)
        handler.on_doctree_read(self.app, document)
        actual = stringtools.normalize(document.pformat())
        target = stringtools.normalize(
            r"""
            <document source="test">
                <literal_block xml:space="preserve">
                    >>> string = 'Hello, world!'
                <literal_block xml:space="preserve">
                    def example_function(expr):
                        r'''This is a multiline docstring.

                        This is the third line of the docstring.
                        '''
                        # This is a comment.
                        print('Entering example function.')
                        try:
                            expr = expr + 1
                        except TypeError:
                            print('Wrong type!')
                        print(expr)
                        print('Leaving example function.')
                <literal_block xml:space="preserve">
                    >>> print(string)
                    Hello, world!
                <literal_block xml:space="preserve">
                    >>> example_function(23)
                    Entering example function.
                    24
                    Leaving example function.
            """)
        assert actual == target

    def test_on_doctree_read_02(self):
        source = r'''
        ..  abjad::

            staff = Staff("c'1 g'1")
            for note in staff:
                show(note)

            len(staff)
        '''
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        actual = stringtools.normalize(document.pformat())
        target = stringtools.normalize(
            r"""
            <document source="test">
                <literal_block xml:space="preserve">
                    >>> staff = Staff("c'1 g'1")
                    >>> for note in staff:
                    ...     show(note)
                    ...
                <abjad_output_block image_layout_specifier image_render_specifier="ImageRenderSpecifier(stylesheet='default.ly')" renderer="lilypond" xml:space="preserve">
                    \version "2.19.0"
                    \language "english"

                    #(ly:set-option 'relative-includes #t)

                    \include "default.ly"

                    \header {
                        tagline = ##f
                    }

                    \layout {}

                    \paper {}

                    \score {
                        {
                            c'1
                        }
                    }
                <abjad_output_block image_layout_specifier image_render_specifier="ImageRenderSpecifier(stylesheet='default.ly')" renderer="lilypond" xml:space="preserve">
                    \version "2.19.0"
                    \language "english"

                    #(ly:set-option 'relative-includes #t)

                    \include "default.ly"

                    \header {
                        tagline = ##f
                    }

                    \layout {}

                    \paper {}

                    \score {
                        {
                            g'1
                        }
                    }
                <literal_block xml:space="preserve">
                    >>> len(staff)
                    2
            """)
        assert actual == target

    def test_on_doctree_read_03(self):
        source = r'''
        ..  abjad::
            :no-stylesheet:

            staff = Staff("c'1 g'1")
            for note in staff:
                show(note)

            len(staff)
        '''
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        actual = stringtools.normalize(document.pformat())
        target = stringtools.normalize(
            r"""
            <document source="test">
                <literal_block xml:space="preserve">
                    >>> staff = Staff("c'1 g'1")
                    >>> for note in staff:
                    ...     show(note)
                    ...
                <abjad_output_block image_layout_specifier image_render_specifier="ImageRenderSpecifier(no_stylesheet=True)" renderer="lilypond" xml:space="preserve">
                    \version "2.19.0"
                    \language "english"

                    \header {
                        tagline = ##f
                    }

                    \layout {}

                    \paper {}

                    \score {
                        {
                            c'1
                        }
                    }
                <abjad_output_block image_layout_specifier image_render_specifier="ImageRenderSpecifier(no_stylesheet=True)" renderer="lilypond" xml:space="preserve">
                    \version "2.19.0"
                    \language "english"

                    \header {
                        tagline = ##f
                    }

                    \layout {}

                    \paper {}

                    \score {
                        {
                            g'1
                        }
                    }
                <literal_block xml:space="preserve">
                    >>> len(staff)
                    2
            """)
        assert actual == target

    def test_on_doctree_read_04(self):
        source = r'''
        ..  container:: example

            **Example 1.** Duple meter:

            ::

                >>> 1 + 1

            ::

                >>> meter = metertools.Meter((2, 4))
                >>> meter
                Meter('(2/4 (1/4 1/4))')
                >>> print(meter.pretty_rtm_format)
                (2/4 (
                    1/4
                    1/4))

            ::

                >>> graph(meter) # doctest: +SKIP

            `2/4` comprises two beats.

        ..  container:: example

            **Example 2.** Triple meter:

            ::

                >>> meter = metertools.Meter((3, 4))
                >>> print(meter.pretty_rtm_format)
                (3/4 (
                    1/4
                    1/4
                    1/4))

            ::

                >>> graph(meter) # doctest: +SKIP

            `3/4` comprises three beats.
        '''
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        actual = stringtools.normalize(document.pformat())
        target = stringtools.normalize(
            r"""
            <document source="test">
                <container classes="example">
                    <paragraph>
                        <strong>
                            Example 1.
                         Duple meter:
                    <literal_block xml:space="preserve">
                        >>> 1 + 1
                        2
                    <literal_block xml:space="preserve">
                        >>> meter = metertools.Meter((2, 4))
                        >>> meter
                        Meter('(2/4 (1/4 1/4))')
                    <literal_block xml:space="preserve">
                        >>> print(meter.pretty_rtm_format)
                        (2/4 (
                            1/4
                            1/4))
                    <literal_block xml:space="preserve">
                        >>> graph(meter) # doctest: +SKIP
                    <abjad_output_block image_layout_specifier image_render_specifier layout="dot" renderer="graphviz" xml:space="preserve">
                        digraph G {
                            graph [bgcolor=transparent,
                                fontname=Arial,
                                penwidth=2,
                                truecolor=true];
                            node [fontname=Arial,
                                fontsize=12,
                                penwidth=2];
                            edge [penwidth=2];
                            node_0 [label="2/4",
                                shape=triangle];
                            node_1 [label="1/4",
                                shape=box];
                            node_2 [label="1/4",
                                shape=box];
                            subgraph cluster_cluster_offsets {
                                graph [style=rounded];
                                node_3_0 [color=white,
                                    fillcolor=black,
                                    fontcolor=white,
                                    fontname="Arial bold",
                                    label="{ <f_0_0> 0 | <f_0_1> ++ }",
                                    shape=Mrecord,
                                    style=filled];
                                node_3_1 [color=white,
                                    fillcolor=black,
                                    fontcolor=white,
                                    fontname="Arial bold",
                                    label="{ <f_0_0> 1/4 | <f_0_1> + }",
                                    shape=Mrecord,
                                    style=filled];
                                node_3_2 [label="{ <f_0_0> 1/2 | <f_0_1> ++ }",
                                    shape=Mrecord];
                            }
                            node_0 -> node_1;
                            node_0 -> node_2;
                            node_1 -> node_3_0 [style=dotted];
                            node_1 -> node_3_1 [style=dotted];
                            node_2 -> node_3_1 [style=dotted];
                            node_2 -> node_3_2 [style=dotted];
                        }
                    <paragraph>
                        <title_reference>
                            2/4
                         comprises two beats.
                <container classes="example">
                    <paragraph>
                        <strong>
                            Example 2.
                         Triple meter:
                    <literal_block xml:space="preserve">
                        >>> meter = metertools.Meter((3, 4))
                        >>> print(meter.pretty_rtm_format)
                        (3/4 (
                            1/4
                            1/4
                            1/4))
                    <literal_block xml:space="preserve">
                        >>> graph(meter) # doctest: +SKIP
                    <abjad_output_block image_layout_specifier image_render_specifier layout="dot" renderer="graphviz" xml:space="preserve">
                        digraph G {
                            graph [bgcolor=transparent,
                                fontname=Arial,
                                penwidth=2,
                                truecolor=true];
                            node [fontname=Arial,
                                fontsize=12,
                                penwidth=2];
                            edge [penwidth=2];
                            node_0 [label="3/4",
                                shape=triangle];
                            node_1 [label="1/4",
                                shape=box];
                            node_2 [label="1/4",
                                shape=box];
                            node_3 [label="1/4",
                                shape=box];
                            subgraph cluster_cluster_offsets {
                                graph [style=rounded];
                                node_4_0 [color=white,
                                    fillcolor=black,
                                    fontcolor=white,
                                    fontname="Arial bold",
                                    label="{ <f_0_0> 0 | <f_0_1> ++ }",
                                    shape=Mrecord,
                                    style=filled];
                                node_4_1 [color=white,
                                    fillcolor=black,
                                    fontcolor=white,
                                    fontname="Arial bold",
                                    label="{ <f_0_0> 1/4 | <f_0_1> + }",
                                    shape=Mrecord,
                                    style=filled];
                                node_4_2 [color=white,
                                    fillcolor=black,
                                    fontcolor=white,
                                    fontname="Arial bold",
                                    label="{ <f_0_0> 1/2 | <f_0_1> + }",
                                    shape=Mrecord,
                                    style=filled];
                                node_4_3 [label="{ <f_0_0> 3/4 | <f_0_1> ++ }",
                                    shape=Mrecord];
                            }
                            node_0 -> node_1;
                            node_0 -> node_2;
                            node_0 -> node_3;
                            node_1 -> node_4_0 [style=dotted];
                            node_1 -> node_4_1 [style=dotted];
                            node_2 -> node_4_1 [style=dotted];
                            node_2 -> node_4_2 [style=dotted];
                            node_3 -> node_4_2 [style=dotted];
                            node_3 -> node_4_3 [style=dotted];
                        }
                    <paragraph>
                        <title_reference>
                            3/4
                         comprises three beats.
            """)
        assert actual == target, \
            systemtools.TestManager.diff(actual, target, 'Diff:')

    def test_on_doctree_read_05(self):
        source = r'''
        ..  abjad::
            :text-width: 40

            [x for x in dir() if not x.startswith('_')]
        '''
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        actual = stringtools.normalize(document.pformat())
        target = stringtools.normalize(
            r"""
            <document source="test">
                <literal_block xml:space="preserve">
                    >>> [x for x in dir() if not x.startswith('_')]
                    ['Accelerando', 'Articulation', 'Beam',
                    'Chord', 'Clef', 'Container', 'Context',
                    'Crescendo', 'Decrescendo', 'Duration',
                    'Dynamic', 'Fermata', 'Fraction',
                    'Glissando', 'Hairpin', 'KeySignature',
                    'LilyPondCommand', 'Markup', 'Measure',
                    'MultimeasureRest', 'Multiplier',
                    'NamedPitch', 'Note', 'Offset', 'Ratio',
                    'Rest', 'Ritardando', 'Score',
                    'Sequence', 'Skip', 'Slur', 'Staff',
                    'StaffGroup', 'Tempo', 'Tie',
                    'TimeSignature', 'Timespan', 'Tuplet',
                    'Voice', 'abctools',
                    'abjad_configuration', 'agenttools',
                    'attach', 'commandlinetools',
                    'datastructuretools', 'demos', 'detach',
                    'documentationtools', 'durationtools',
                    'exceptiontools', 'expressiontools',
                    'ext', 'f', 'graph', 'indicatortools',
                    'inspect_', 'instrumenttools',
                    'ipythontools', 'iterate', 'label',
                    'lilypondfiletools',
                    'lilypondnametools',
                    'lilypondparsertools', 'ly',
                    'markuptools', 'mathtools',
                    'metertools', 'mutate', 'new',
                    'override', 'parse', 'patterntools',
                    'persist', 'pitchtools', 'play',
                    'print_function', 'quantizationtools',
                    'rhythmmakertools', 'rhythmtreetools',
                    'schemetools', 'scoretools', 'select',
                    'selectiontools', 'selectortools',
                    'sequence', 'sequencetools', 'set_',
                    'show', 'spannertools', 'stringtools',
                    'systemtools', 'templatetools',
                    'timespantools', 'tonalanalysistools',
                    'topleveltools']
            """)
        assert actual == target, \
            systemtools.TestManager.diff(actual, target, 'Diff:')

    def test_on_doctree_read_06(self):
        source = u'''
        This example demonstrates the power of exploiting redundancy to model
        musical structure. The piece that concerns us here is Ligeti's *Désordre*:
        the first piano study from Book I. Specifically, we will focus on modeling
        the first section of the piece.

        ..  abjad::

            print('Désordre')
        '''
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        actual = stringtools.normalize(document.pformat())
        target = stringtools.normalize(
            u"""
            <document source="test">
                <paragraph>
                    This example demonstrates the power of exploiting redundancy to model
                    musical structure. The piece that concerns us here is Ligeti's
                    <emphasis>
                        Désordre
                    :
                    the first piano study from Book I. Specifically, we will focus on modeling
                    the first section of the piece.
                <literal_block xml:space="preserve">
                    >>> print('Désordre')
                    Désordre
            """)
        assert actual == target, \
            systemtools.TestManager.diff(actual, target, 'Diff:')

    def test_on_doctree_read_07(self):
        source = '''
        ..  abjad::
            :hide:
            :no-trim:
            :pages: 1-4
            :with-columns: 2

            show(Staff("c'4 d'4 e'4 f'4"))
        '''
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        actual = stringtools.normalize(document.pformat())
        target = stringtools.normalize(
            r"""
            <document source="test">
                <block_quote>
                    <abjad_output_block image_layout_specifier="ImageLayoutSpecifier(pages=(1, 2, 3, 4), with_columns=2)" image_render_specifier="ImageRenderSpecifier(no_trim=True, stylesheet='default.ly')" renderer="lilypond" xml:space="preserve">
                        \version "2.19.0"
                        \language "english"

                        #(ly:set-option 'relative-includes #t)

                        \include "default.ly"

                        \header {
                            tagline = ##f
                        }

                        \layout {}

                        \paper {}

                        \score {
                            \new Staff {
                                c'4
                                d'4
                                e'4
                                f'4
                            }
                        }
            """)
        assert actual == target, \
            systemtools.TestManager.diff(actual, target, 'Diff:')

    def test_on_doctree_read_08(self):
        source = '''
        ..  abjad::

            staff = Staff("c'4 d'4 e'4 f'4")
            spanner = Slur()
            attach(spanner, staff[:])

        ..  abjad::

            for leaf in staff:
                is_first = spanner._is_my_first_leaf(leaf)
                is_last = spanner._is_my_last_leaf(leaf)
                print(repr(leaf), is_first, is_last)
        '''
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        actual = stringtools.normalize(document.pformat())
        target = stringtools.normalize(
            r"""
            <document source="test">
                <block_quote>
                    <literal_block xml:space="preserve">
                        >>> staff = Staff("c'4 d'4 e'4 f'4")
                        >>> spanner = Slur()
                        >>> attach(spanner, staff[:])
                    <literal_block xml:space="preserve">
                        >>> for leaf in staff:
                        ...     is_first = spanner._is_my_first_leaf(leaf)
                        ...     is_last = spanner._is_my_last_leaf(leaf)
                        ...     print(repr(leaf), is_first, is_last)
                        ...
                        Note("c'4") True False
                        Note("d'4") False False
                        Note("e'4") False False
                        Note("f'4") False True
            """)
        assert actual == target, \
            systemtools.TestManager.diff(actual, target, 'Diff:')

    def test_on_doctree_read_09(self):
        source = '''
        ..  abjad::
            :strip-prompt:

            class Foo(object):

                def bar(self):
                    print('OK')

                def baz(self):
                    print('NO')

                def quux(self):
                    return 23

        ..  abjad::

            foo = Foo()
            foo.quux()
        '''
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        actual = stringtools.normalize(document.pformat())
        target = stringtools.normalize(
            r"""
            <document source="test">
                <block_quote>
                    <literal_block xml:space="preserve">
                        class Foo(object):

                            def bar(self):
                                print('OK')

                            def baz(self):
                                print('NO')

                            def quux(self):
                                return 23
                    <literal_block xml:space="preserve">
                        >>> foo = Foo()
                        >>> foo.quux()
                        23
            """)
        assert actual == target, \
            systemtools.TestManager.diff(actual, target, 'Diff:')

    def test_on_doctree_read_10(self):
        source = '''
        ..  abjad::
            :hide:
            :reveal-label: foo
            :strip-prompt:

            def foo(x):
                return x + 1

        ..  abjad::

            3 * 5

        ..  reveal:: foo

        ..  abjad::

            foo(23)
        '''
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        actual = stringtools.normalize(document.pformat())
        target = stringtools.normalize(
            r"""
            <document source="test">
                <block_quote>
                    <literal_block xml:space="preserve">
                        >>> 3 * 5
                        15
                    <literal_block xml:space="preserve">
                        def foo(x):
                            return x + 1
                    <literal_block xml:space="preserve">
                        >>> foo(23)
                        24
            """)
        assert actual == target, \
            systemtools.TestManager.diff(actual, target, 'Diff:')