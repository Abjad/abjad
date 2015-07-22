# -*- encoding: utf-8 -*-
from abjad.tools import abjadbooktools
import unittest
from abjad.tools import systemtools


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
    source_one = systemtools.TestManager.clean_string(source_one)

    source_two = r'''
    ..  abjad::

        staff = Staff("c'1 g'1")
        for note in staff:
            show(note)

        len(staff)
    '''
    source_two = systemtools.TestManager.clean_string(source_two)

    source_three = r'''
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
    source_three = systemtools.TestManager.clean_string(source_three)

    source_four = r'''
    ..  abjad::
        :text-width: 40

        dir()
    '''
    source_four = systemtools.TestManager.clean_string(source_four)

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
        actual = systemtools.TestManager.clean_string(document.pformat())
        target = systemtools.TestManager.clean_string(
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
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(self.source_two)
        handler.on_doctree_read(self.app, document)
        actual = systemtools.TestManager.clean_string(document.pformat())
        target = systemtools.TestManager.clean_string(
            r"""
            <document source="test">
                <literal_block xml:space="preserve">
                    >>> staff = Staff("c'1 g'1")
                    >>> for note in staff:
                    ...     show(note)
                    ...
                <abjad_output_block renderer="lilypond" xml:space="preserve">
                    \version "2.19.0"
                    \language "english"

                    #(set-global-staff-size 12)

                    \header {
                        tagline = \markup {}
                    }

                    \layout {
                        indent = #0
                        ragged-right = ##t
                        \context {
                            \Score
                            \remove Bar_number_engraver
                            \override SpacingSpanner #'strict-grace-spacing = ##t
                            \override SpacingSpanner #'strict-note-spacing = ##t
                            \override SpacingSpanner #'uniform-stretching = ##t
                            \override TupletBracket #'bracket-visibility = ##t
                            \override TupletBracket #'minimum-length = #3
                            \override TupletBracket #'padding = #2
                            \override TupletBracket #'springs-and-rods = #ly:spanner::set-spacing-rods
                            \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                            proportionalNotationDuration = #(ly:make-moment 1 24)
                            tupletFullLength = ##t
                        }
                    }

                    \paper {
                        left-margin = 1\in
                    }

                    \score {
                        {
                            c'1
                        }
                    }
                <abjad_output_block renderer="lilypond" xml:space="preserve">
                    \version "2.19.0"
                    \language "english"

                    #(set-global-staff-size 12)

                    \header {
                        tagline = \markup {}
                    }

                    \layout {
                        indent = #0
                        ragged-right = ##t
                        \context {
                            \Score
                            \remove Bar_number_engraver
                            \override SpacingSpanner #'strict-grace-spacing = ##t
                            \override SpacingSpanner #'strict-note-spacing = ##t
                            \override SpacingSpanner #'uniform-stretching = ##t
                            \override TupletBracket #'bracket-visibility = ##t
                            \override TupletBracket #'minimum-length = #3
                            \override TupletBracket #'padding = #2
                            \override TupletBracket #'springs-and-rods = #ly:spanner::set-spacing-rods
                            \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                            proportionalNotationDuration = #(ly:make-moment 1 24)
                            tupletFullLength = ##t
                        }
                    }

                    \paper {
                        left-margin = 1\in
                    }

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
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(self.source_three)
        handler.on_doctree_read(self.app, document)
        actual = systemtools.TestManager.clean_string(document.pformat())
        target = systemtools.TestManager.clean_string(
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
                    <abjad_output_block renderer="graphviz" xml:space="preserve">
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
                    <abjad_output_block renderer="graphviz" xml:space="preserve">
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
        assert actual == target

    def test_on_doctree_read_04(self):
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(self.source_four)
        handler.on_doctree_read(self.app, document)
        actual = systemtools.TestManager.clean_string(document.pformat())
        target = systemtools.TestManager.clean_string(
            r"""
            <document source="test">
                <literal_block xml:space="preserve">
                    >>> dir()
                    ['Accelerando', 'Articulation', 'Beam',
                    'Chord', 'Clef', 'Container', 'Context',
                    'Crescendo', 'Decrescendo', 'Duration',
                    'Dynamic', 'Fermata', 'Fraction',
                    'Glissando', 'Hairpin', 'KeySignature',
                    'Markup', 'Measure', 'MultimeasureRest',
                    'Multiplier', 'NamedPitch', 'Note',
                    'Offset', 'Rest', 'Ritardando', 'Score',
                    'Sequence', 'Skip', 'Slur', 'Staff',
                    'StaffGroup', 'Tempo', 'Tie',
                    'TimeSignature', 'Timespan', 'Tuplet',
                    'Voice', '__builtins__', '__cached__',
                    '__doc__', '__file__', '__loader__',
                    '__name__', '__package__', '__path__',
                    '__spec__', '__version__',
                    '__version_info__', 'abctools',
                    'abjad_configuration', 'abjadbooktools',
                    'agenttools', 'attach',
                    'datastructuretools', 'detach',
                    'developerscripttools',
                    'documentationtools', 'durationtools',
                    'exceptiontools', 'f', 'graph',
                    'handlertools', 'indicatortools',
                    'inspect_', 'instrumenttools',
                    'ipythontools', 'iterate', 'labeltools',
                    'layouttools', 'lilypondfiletools',
                    'lilypondnametools',
                    'lilypondparsertools', 'ly',
                    'markuptools', 'mathtools',
                    'metertools', 'mutate', 'new',
                    'override', 'parse', 'persist',
                    'pitchtools', 'play',
                    'quantizationtools', 'quit',
                    'rhythmmakertools', 'rhythmtreetools',
                    'schemetools', 'scoretools', 'select',
                    'selectiontools', 'selectortools',
                    'sequencetools', 'set_', 'show',
                    'sievetools', 'spannertools',
                    'stringtools', 'systemtools',
                    'templatetools', 'timespantools',
                    'tonalanalysistools', 'topleveltools']
            """)
        assert actual == target