"""
Tools for modeling IRCAM-style rhythm trees.
"""

import fractions
import typing

import uqbar.containers
import uqbar.graphs

from . import duration as _duration
from . import makers as _makers
from . import math as _math
from . import mutate as _mutate
from . import score as _score
from . import select as _select
from . import sequence as _sequence
from . import spanners as _spanners
from .parsers.base import Parser


class RhythmTreeNode:
    """
    Rhythm-tree node.
    """

    ### CLASS VARIABLES ###

    _is_abstract = True
    _state_flag_names: tuple[str, ...] = ("_offsets_are_current",)

    ### INITIALIZER ###

    def __init__(self, pair: tuple[int, int]) -> None:
        assert isinstance(pair, tuple), repr(pair)
        self._offset = _duration.Offset(0)
        self._offsets_are_current = False
        self._pair = (0, 1)
        self.pair = pair

    ### PRIVATE METHODS ###

    def _depthwise_inventory(self):
        def recurse(node):
            if node.depth not in inventory:
                inventory[node.depth] = []
            inventory[node.depth].append(node)
            if getattr(node, "children", None) is not None:
                for child in node.children:
                    recurse(child)

        inventory = {}
        recurse(self)
        return inventory

    def _get_fraction_string(self):
        n, d = self.pair
        if d == 1:
            string = str(n)
        else:
            string = f"{n}/{d}"
        return string

    def _get_parentage_ratios(self) -> tuple[tuple[int, int], ...]:
        result = []
        node = self
        assert hasattr(node, "parent"), repr(node)
        while node.parent is not None:
            pair = _duration.Duration(node.pair)
            parent_contents_duration = node.parent._get_contents_duration()
            fraction = pair / parent_contents_duration
            assert isinstance(fraction, fractions.Fraction), repr(fraction)
            duration = _duration.Duration(fraction)
            assert isinstance(duration, _duration.Duration), repr(duration)
            result.append(duration.pair)
            node = node.parent
        pair = _duration.Duration(node.pair)
        result.append(pair.pair)
        return tuple(reversed(result))

    def _update_offsets_of_entire_tree(self):
        def recurse(container, current_offset):
            container._offset = current_offset
            container._offsets_are_current = True
            for child in container:
                if getattr(child, "children", None) is not None:
                    current_offset = recurse(child, current_offset)
                else:
                    child._offset = current_offset
                    child._offsets_are_current = True
                    current_offset += _duration.Duration(child.duration)
            return current_offset

        offset = _duration.Offset(0)
        root = self.root
        if root is None:
            root = self
        if root is self and not hasattr(self, "children"):
            self._offset = offset
            self._offsets_are_current = True
        else:
            recurse(root, offset)

    def _update_offsets_of_entire_tree_if_necessary(self):
        if not self._get_node_state_flags()["_offsets_are_current"]:
            self._update_offsets_of_entire_tree()

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self) -> _duration.Duration:
        r"""
        Gets duration of rhythm-tree node.

        ..  container:: example

            >>> string = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> rtc = abjad.rhythmtrees.parse(string)[0]
            >>> components = rtc(abjad.Duration(1, 1))
            >>> voice = abjad.Voice(components)
            >>> score = abjad.Score([voice])
            >>> abjad.setting(score).proportionalNotationDuration = "#1/12"
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                \with
                {
                    proportionalNotationDuration = #1/12
                }
                <<
                    \new Voice
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 1/1
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \tuplet 1/1
                            {
                                c'4
                                c'4
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \tuplet 1/1
                            {
                                c'4
                                c'4
                            }
                        }
                    }
                >>

            >>> rtc.duration
            Duration(1, 1)

            >>> rtc[1].duration
            Duration(1, 2)

            >>> rtc[1][1].duration
            Duration(1, 4)

        """
        numerator = self.prolation.numerator * self.pair[0]
        denominator = self.prolation.denominator * self.pair[1]
        return _duration.Duration((numerator, denominator))

    @property
    def pair(self) -> tuple[int, int]:
        """
        Gets pair of rhythm-tree node.

        ..  container:: example

            >>> abjad.rhythmtrees.RhythmTreeLeaf((1, 1)).pair
            (1, 1)

            >>> abjad.rhythmtrees.RhythmTreeLeaf((2, 4)).pair
            (2, 4)

        """
        return self._pair

    @pair.setter
    def pair(self, pair):
        assert isinstance(pair, tuple), repr(pair)
        assert 0 < fractions.Fraction(*pair)
        self._pair = pair
        self._mark_entire_tree_for_later_update()

    @property
    def pretty_rtm_format(self) -> str:
        """
        Gets pretty-printed RTM format of rhythm-tree node.

        ..  container:: example

            >>> string = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> rtc = abjad.rhythmtrees.parse(string)[0]

            >>> print(rtc.pretty_rtm_format)
            (1 (
                (1 (
                    1
                    1))
                (1 (
                    1
                    1))))

            >>> print(rtc[0].pretty_rtm_format)
            (1 (
                1
                1))

            >>> print(rtc[0][0].pretty_rtm_format)
            1

        """
        assert hasattr(self, "_pretty_rtm_format_pieces"), repr(self)
        return "\n".join(self._pretty_rtm_format_pieces())

    @property
    def prolation(self) -> fractions.Fraction:
        """
        Gets prolation of rhythm-tree node.
        """
        return _math.cumulative_products(self.prolations)[-1]

    @property
    def prolations(self) -> tuple[fractions.Fraction, ...]:
        """
        Gets prolations of rhythm-tree node.
        """
        prolations = [fractions.Fraction(1)]
        assert hasattr(self, "parentage")
        pairs = _sequence.nwise(self.parentage)
        for child, parent in pairs:
            parent_contents_duration = parent._get_contents_duration()
            assert isinstance(parent_contents_duration, _duration.Duration)
            parent_preprolated_duration = _duration.Duration(parent.pair)
            duration = parent_preprolated_duration / parent_contents_duration
            prolation = fractions.Fraction(duration)
            prolations.append(prolation)
        return tuple(prolations)

    @property
    def start_offset(self) -> _duration.Offset:
        """
        Gets start offset of rhythm-tree node.

        ..  container:: example

            >>> string = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> rtc = abjad.rhythmtrees.parse(string)[0]

            >>> rtc.start_offset
            Offset((0, 1))

            >>> rtc[1].start_offset
            Offset((1, 2))

            >>> rtc[1][1].start_offset
            Offset((3, 4))

        """
        self._update_offsets_of_entire_tree_if_necessary()
        return self._offset

    @property
    def stop_offset(self) -> _duration.Offset:
        """
        Gets stop offset of rhythm-tree node.

        ..  container:: example

            >>> string = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> rtc = abjad.rhythmtrees.parse(string)[0]

            >>> rtc.stop_offset
            Offset((1, 1))

            >>> rtc[0].stop_offset
            Offset((1, 2))

            >>> rtc[0][0].stop_offset
            Offset((1, 4))

        """
        return self.start_offset + _duration.Duration(self.duration)


class RhythmTreeLeaf(RhythmTreeNode, uqbar.containers.UniqueTreeNode):
    r"""
    Rhythm-tree leaf.

    ..  container:: example

        Pitched rhythm-tree leaves makes notes:

        >>> rtl = abjad.rhythmtrees.RhythmTreeLeaf((5, 1), is_pitched=True)
        >>> components = rtl(abjad.Duration(1, 4))
        >>> voice = abjad.Voice(components)
        >>> abjad.setting(voice[0]).Score.proportionalNotationDuration = "#1/12"
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \set Score.proportionalNotationDuration = #1/12
                c'1
                ~
                c'4
            }

    ..  container:: example

        Unpitched rhythm-tree leaves make rests:

        >>> rtl = abjad.rhythmtrees.RhythmTreeLeaf((5, 1), is_pitched=False)
        >>> components = rtl(abjad.Duration(1, 4))
        >>> voice = abjad.Voice(components)
        >>> abjad.setting(voice[0]).Score.proportionalNotationDuration = "#1/12"
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \set Score.proportionalNotationDuration = #1/12
                r1
                r4
            }


    """

    def __init__(
        self,
        pair: tuple[int, int],
        *,
        is_pitched: bool = True,
        name: str | None = None,
    ) -> None:
        assert isinstance(pair, tuple), repr(pair)
        uqbar.containers.UniqueTreeNode.__init__(self, name=name)
        RhythmTreeNode.__init__(self, pair)
        self.is_pitched = is_pitched

    def __call__(
        self, duration: _duration.Duration
    ) -> list[_score.Leaf | _score.Tuplet]:
        """
        Makes list of leaves and / or tuplets equal to ``duration``.
        """
        assert isinstance(duration, _duration.Duration), repr(duration)
        pitches: list[int | None]
        if self.is_pitched:
            pitches = [0]
        else:
            pitches = [None]
        duration *= _duration.Duration(self.pair)
        components = _makers.make_leaves(pitches, duration)
        return components

    def __graph__(self, **keywords) -> uqbar.graphs.Graph:
        """
        Gets Graphviz graph of rhythm-tree leaf.
        """
        graph = uqbar.graphs.Graph(name="G")
        label = str(_duration.Duration(self.pair))
        node = uqbar.graphs.Node(attributes={"label": label, "shape": "box"})
        graph.append(node)
        return graph

    def __repr__(self) -> str:
        """
        Gets interpreter representation of rhythm-tree leaf.
        """
        properties = [
            f"{self.pair!r}",
            f"is_pitched={self.is_pitched!r}",
        ]
        if self.name is not None:
            properties.append(f"name={self.name!r}")
        properties_string = ", ".join(properties)
        return f"{type(self).__name__}({properties_string})"

    def _pretty_rtm_format_pieces(self):
        return [str(self._get_fraction_string())]

    @property
    def is_pitched(self) -> bool:
        """
        Is true when rhythm-tree leaf is pitched.
        """
        return self._is_pitched

    @is_pitched.setter
    def is_pitched(self, argument):
        self._is_pitched = bool(argument)

    @property
    def rtm_format(self) -> str:
        """
        Gets RTM format of rhythm-tree leaf.

        ..  container:: example

            >>> abjad.rhythmtrees.RhythmTreeLeaf((5, 1), is_pitched=True).rtm_format
            '5'

            >>> abjad.rhythmtrees.RhythmTreeLeaf((5, 1), is_pitched=False).rtm_format
            '-5'

        """
        string = self._get_fraction_string()
        if self.is_pitched:
            return f"{string!s}"
        return f"-{string!s}"


class RhythmTreeContainer(RhythmTreeNode, uqbar.containers.UniqueTreeList):
    r"""
    Rhythm-tree container.

    ..  container:: example

        Extend rhythm-tree containers with rhythm-tree leaves or other
        rhythm-tree containers:

        >>> rtc = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
        >>> rtc.append(abjad.rhythmtrees.RhythmTreeLeaf((1, 1)))
        >>> rtc.append(abjad.rhythmtrees.RhythmTreeLeaf((2, 1)))
        >>> rtc.append(abjad.rhythmtrees.RhythmTreeLeaf((2, 1)))

        Use RTM format strings to view the structure of rhythm-tree containers:

        >>> print(rtc.rtm_format)
        (1 (1 2 2))

        >>> print(rtc.pretty_rtm_format)
        (1 (
            1
            2
            2))

        Call rhythm-tree containers with a duration to make components:

        >>> components = rtc(abjad.Duration(1, 1))
        >>> voice = abjad.Voice(components)
        >>> abjad.setting(voice[0]).Score.proportionalNotationDuration = "#1/12"
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \set Score.proportionalNotationDuration = #1/12
                \tuplet 5/4
                {
                    c'4
                    c'2
                    c'2
                }
            }

    """

    ### INITIALIZER ###

    def __init__(
        self,
        pair: tuple[int, int],
        children: typing.Sequence[RhythmTreeNode] = (),
        *,
        name: str = "",
    ):
        assert isinstance(pair, tuple), repr(pair)
        uqbar.containers.UniqueTreeList.__init__(self, name=name)
        RhythmTreeNode.__init__(self, pair)
        self.extend(children)

    ### SPECIAL METHODS ###

    def __add__(self, rtc: "RhythmTreeContainer") -> "RhythmTreeContainer":
        r"""
        Concatenates ``self`` and ``rtc``.

        The operation ``a + b = c`` returns a new rhythm-tree container ``c``
        with the contents of ``a`` followed by the contents of ``b``; the
        operation is noncommutative.


        ..  container:: example

            >>> rtc_a = abjad.rhythmtrees.parse('(1 (1 1 1))')[0]
            >>> components = rtc_a(abjad.Duration(1, 2))
            >>> voice = abjad.Voice(components)
            >>> leaf = abjad.select.leaf(voice, 0)
            >>> abjad.setting(leaf).Score.proportionalNotationDuration = "#1/12"
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    \tuplet 3/2
                    {
                        \set Score.proportionalNotationDuration = #1/12
                        c'4
                        c'4
                        c'4
                    }
                }

            >>> rtc_b = abjad.rhythmtrees.parse('(1 (3 4))')[0]
            >>> components = rtc_b(abjad.Duration(1, 2))
            >>> voice = abjad.Voice(components)
            >>> leaf = abjad.select.leaf(voice, 0)
            >>> abjad.setting(leaf).Score.proportionalNotationDuration = "#1/12"
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    \tuplet 7/4
                    {
                        \set Score.proportionalNotationDuration = #1/12
                        c'4.
                        c'2
                    }
                }

            >>> rtc_c = rtc_a + rtc_b
            >>> components = rtc_c(abjad.Duration(1, 2))
            >>> voice = abjad.Voice(components)
            >>> leaf = abjad.select.leaf(voice, 0)
            >>> abjad.setting(leaf).Score.proportionalNotationDuration = "#1/12"
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    \tuplet 5/4
                    {
                        \set Score.proportionalNotationDuration = #1/12
                        c'8
                        c'8
                        c'8
                        c'4.
                        c'2
                    }
                }

            The pair of ``c`` equals the sum of the pairs of ``a`` and ``b``:

            >>> rtc_a.pair
            (1, 1)

            >>> rtc_b.pair
            (1, 1)

            >>> rtc_c.pair
            (2, 1)

        """
        assert isinstance(rtc, RhythmTreeContainer), repr(rtc)
        new_duration = _duration.Duration(self.duration)
        new_duration += _duration.Duration(rtc.duration)
        container = RhythmTreeContainer(new_duration.pair)
        container.extend(self[:])
        container.extend(rtc[:])
        return container

    def __call__(
        self, duration: _duration.Duration
    ) -> list[_score.Leaf | _score.Tuplet]:
        r"""
        Makes list of leaves and / or tuplets equal to ``duration``.

        ..  container:: example

            >>> string = '(1 (1 (2 (1 1 1)) 2))'
            >>> rtc = abjad.rhythmtrees.parse(string)[0]
            >>> components = rtc(abjad.Duration(1, 1))
            >>> voice = abjad.Voice(components)
            >>> abjad.setting(voice[0]).proportionalNotationDuration = "#1/12"
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    \set proportionalNotationDuration = #1/12
                    \tuplet 5/4
                    {
                        c'4
                        \tuplet 3/2
                        {
                            c'4
                            c'4
                            c'4
                        }
                        c'2
                    }
                }

        """
        assert isinstance(duration, _duration.Duration), repr(duration)
        assert 0 < duration

        def recurse(rtc, tuplet_duration):
            assert isinstance(rtc, RhythmTreeContainer), repr(rtc)
            assert isinstance(tuplet_duration, _duration.Duration)
            contents_duration = rtc._get_contents_duration()
            basic_prolated_fraction = tuplet_duration / contents_duration
            assert isinstance(basic_prolated_fraction, fractions.Fraction)
            basic_written_duration = _duration.Duration(basic_prolated_fraction)
            basic_written_duration = (
                basic_written_duration.equal_or_greater_power_of_two
            )
            assert isinstance(basic_written_duration, _duration.Duration)
            tuplet = _score.Tuplet((1, 1), [])
            for node in rtc.children:
                if isinstance(node, type(self)):
                    tuplet_duration_ = _duration.Duration(node.pair)
                    tuplet_duration_ *= basic_written_duration
                    components = recurse(node, tuplet_duration_)
                    tuplet.extend(components)
                else:
                    leaves = node(basic_written_duration)
                    tuplet.extend(leaves)
                    if 1 < len(leaves):
                        _spanners.tie(leaves)
            assert fractions.Fraction(*tuplet.multiplier) == 1, repr(tuplet.multiplier)
            contents_duration = tuplet._get_duration()
            target_duration = tuplet_duration
            multiplier = target_duration / contents_duration
            tuplet.multiplier = _duration.pair(multiplier)
            return [tuplet]

        tuplet_duration_ = duration * _duration.Duration(self.pair)
        assert isinstance(tuplet_duration_, _duration.Duration)
        components = recurse(self, tuplet_duration_)
        assert all(isinstance(_, _score.Leaf | _score.Tuplet) for _ in components)
        return components

    def __graph__(self, **keywords) -> uqbar.graphs.Graph:
        r"""
        Graphs rhythm-tree container.

        ..  container:: example

            >>> string = '(1 (1 (2 (1 1 1)) 2))'
            >>> rtc = abjad.rhythmtrees.parse(string)[0]
            >>> abjad.graph(rtc) # doctest: +SKIP

            ..  docs::

                >>> graph = rtc.__graph__()
                >>> string = format(graph, "graphviz")
                >>> print(string)
                digraph G {
                    graph [bgcolor=transparent,
                        truecolor=true];
                    node_0 [label="1",
                        shape=triangle];
                    node_1 [label="1",
                        shape=box];
                    node_2 [label="2",
                        shape=triangle];
                    node_3 [label="1",
                        shape=box];
                    node_4 [label="1",
                        shape=box];
                    node_5 [label="1",
                        shape=box];
                    node_6 [label="2",
                        shape=box];
                    node_0 -> node_1;
                    node_0 -> node_2;
                    node_0 -> node_6;
                    node_2 -> node_3;
                    node_2 -> node_4;
                    node_2 -> node_5;
                }

        """
        graph = uqbar.graphs.Graph(
            name="G",
            attributes={"bgcolor": "transparent", "truecolor": True},
        )
        node_mapping = {}
        nodes = [self]
        nodes.extend(self.depth_first())
        for node in nodes:
            graphviz_node = uqbar.graphs.Node()
            label = str(_duration.Duration(node.pair))
            graphviz_node.attributes["label"] = label
            if isinstance(node, type(self)):
                graphviz_node.attributes["shape"] = "triangle"
            else:
                graphviz_node.attributes["shape"] = "box"
            graph.append(graphviz_node)
            node_mapping[node] = graphviz_node
            if node.parent is not None:
                uqbar.graphs.Edge().attach(
                    node_mapping[node.parent], node_mapping[node]
                )
        return graph

    def __radd__(self, rtc) -> "RhythmTreeContainer":
        """
        Adds ``rtc`` and ``self``.
        """
        assert isinstance(rtc, type(self))
        return rtc.__add__(self)

    def __repr__(self) -> str:
        """
        Gets interpreter representation of rhythm-tree container.
        """
        return f"{type(self).__name__}({self.pair})"

    ### PRIVATE METHODS ###

    def _get_contents_duration(self):
        durations = [_duration.Duration(_.pair) for _ in self]
        duration = sum(durations)
        return duration

    def _prepare_setitem_multiple(self, expr):
        if isinstance(expr, str):
            expr = RhythmTreeParser()(expr)
        elif isinstance(expr, list) and len(expr) == 1 and isinstance(expr[0], str):
            expr = RhythmTreeParser()(expr[0])
        return expr

    def _prepare_setitem_single(self, expr):
        if isinstance(expr, str):
            expr = RhythmTreeParser()(expr)[0]
            assert len(expr) == 1
            expr = expr[0]
        return expr

    def _pretty_rtm_format_pieces(self):
        result = []
        result.append(f"({self._get_fraction_string()} (")
        for child in self:
            result.extend(["    " + x for x in child._pretty_rtm_format_pieces()])
        result[-1] = result[-1] + "))"
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def rtm_format(self) -> str:
        """
        Gets RTM format of rhythm-tree container.

        ..  container:: example

            >>> string = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> rtc = abjad.rhythmtrees.parse(string)[0]

            >>> rtc.rtm_format
            '(1 ((1 (1 1)) (1 (1 1))))'

            >>> rtc[0].rtm_format
            '(1 (1 1))'

            >>> rtc[0][0].rtm_format
            '1'

        """
        string = " ".join([x.rtm_format for x in self])
        fraction_string = self._get_fraction_string()
        return f"({fraction_string} ({string}))"


class RhythmTreeParser(Parser):
    r"""
    Rhythm-tree parser.

    Parses a microlanguage resembling Ircam’s Lisp-based RTM syntax. Generates
    a list of rhythm trees. Composers can manipulate rhythm trees and convert
    them to score components.

    ..  container:: example

        >>> parser = abjad.rhythmtrees.RhythmTreeParser()
        >>> string = '(3 (1 (1 ((2 (1 1 1)) 2 2 1))))'
        >>> rtc = parser(string)[0]

        >>> print(rtc.pretty_rtm_format)
        (3 (
            1
            (1 (
                (2 (
                    1
                    1
                    1))
                2
                2
                1))))

        >>> components = rtc(abjad.Duration(1, 2))
        >>> voice = abjad.Voice(components)
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).proportionalNotationDuration = "#1/12"
        >>> time_signature = abjad.TimeSignature((6, 4))
        >>> leaf = abjad.select.leaf(voice, 0)
        >>> abjad.attach(time_signature, leaf)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                proportionalNotationDuration = #1/12
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 4/3
                        {
                            \time 6/4
                            c'1
                            \tuplet 7/4
                            {
                                \tuplet 3/2
                                {
                                    c'4
                                    c'4
                                    c'4
                                }
                                c'2
                                c'2
                                c'4
                            }
                        }
                    }
                }
            >>

    """

    ### PUBLIC PROPERTIES ###

    @property
    def lexer_rules_object(self):
        return self

    @property
    def parser_rules_object(self):
        return self

    ### LEX SETUP ###

    tokens = ("DURATION", "LPAREN", "RPAREN")

    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_ignore = " \n\t\r"

    ### YACC SETUP ###

    start = "toplevel"

    ### LEX METHODS ###

    def t_DURATION(self, t):
        r"-?[1-9]\d*(/[1-9]\d*)?"
        parts = t.value.partition("/")
        if not parts[2]:
            t.value = _duration.Duration(int(parts[0]))
        else:
            numerator, denominator = int(parts[0]), int(parts[2])
            duration = _duration.Duration(numerator, denominator)
            if numerator == duration.numerator:
                t.value = duration
            else:
                t.value = (numerator, denominator)
        return t

    def t_error(self, t):
        print(("Illegal character '%s'" % t.value[0]))
        t.lexer.skip(1)

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += t.value.count("\n")

    ### YACC METHODS ###

    def p_container__LPAREN__DURATION__node_list_closed__RPAREN(self, p):
        """
        container : LPAREN DURATION node_list_closed RPAREN
        """
        if isinstance(p[2], tuple):
            pair = p[2]
        else:
            assert isinstance(p[2], _duration.Duration)
            pair = p[2].pair
        p[0] = RhythmTreeContainer(pair, children=p[3])

    def p_error(self, p):
        if p:
            print(("Syntax error at '%s'" % p.value))
        else:
            print("Syntax error at EOF")

    def p_leaf__INTEGER(self, p):
        """
        leaf : DURATION
        """
        if isinstance(p[1], int):
            pair = (abs(p[1]), 1)
        else:
            assert isinstance(p[1], _duration.Duration), repr(p[1])
            pair = abs(p[1]).pair
        p[0] = RhythmTreeLeaf(pair, is_pitched=0 < p[1])

    def p_node__container(self, p):
        """
        node : container
        """
        p[0] = p[1]

    def p_node__leaf(self, p):
        """
        node : leaf
        """
        p[0] = p[1]

    def p_node_list__node_list__node_list_item(self, p):
        """
        node_list : node_list node_list_item
        """
        p[0] = p[1] + [p[2]]

    def p_node_list__node_list_item(self, p):
        """
        node_list : node_list_item
        """
        p[0] = [p[1]]

    def p_node_list_closed__LPAREN__node_list__RPAREN(self, p):
        """
        node_list_closed : LPAREN node_list RPAREN
        """
        p[0] = p[2]

    def p_node_list_item__node(self, p):
        """
        node_list_item : node
        """
        p[0] = p[1]

    def p_toplevel__EMPTY(self, p):
        """
        toplevel :
        """
        p[0] = []

    def p_toplevel__toplevel__node(self, p):
        """
        toplevel : toplevel node
        """
        p[0] = p[1] + [p[2]]


def call(
    nodes, duration: _duration.Duration = _duration.Duration(1, 4)
) -> list[_score.Leaf | _score.Tuplet]:
    """
    Calls each node in ``nodes`` with ``duration``.
    """
    assert all(isinstance(_, RhythmTreeContainer | RhythmTreeLeaf) for _ in nodes)
    assert isinstance(duration, _duration.Duration), repr(duration)
    components = []
    for node in nodes:
        components_ = node(duration)
        components.extend(components_)
    prototype_ = (_score.Leaf, _score.Tuplet)
    assert all(isinstance(_, prototype_) for _ in components), repr(components)
    return components


def parse(string: str) -> list[RhythmTreeContainer | RhythmTreeLeaf]:
    r"""
    Parses RTM ``string``.

    ..  container:: example

        Quarter note:

        >>> nodes = abjad.rhythmtrees.parse("1")
        >>> components = abjad.rhythmtrees.call(nodes)
        >>> voice = abjad.Voice(components)
        >>> abjad.setting(voice[0]).Score.proportionalNotationDuration = "#1/12"
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \set Score.proportionalNotationDuration = #1/12
                c'4
            }

    ..  container:: example

        Series of quarter notes:

        >>> nodes = abjad.rhythmtrees.parse("1 1 1 1 1 1")
        >>> components = abjad.rhythmtrees.call(nodes)
        >>> voice = abjad.Voice(components)
        >>> abjad.setting(voice[0]).Score.proportionalNotationDuration = "#1/12"
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \set Score.proportionalNotationDuration = #1/12
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
            }

    ..  container:: example

        Half-note duration divided into 1 part:

        >>> string = "(2 (1))"
        >>> nodes = abjad.rhythmtrees.parse(string)
        >>> components = abjad.rhythmtrees.call(nodes)
        >>> voice = abjad.Voice(components)
        >>> leaf = abjad.select.leaf(voice, 0)
        >>> abjad.setting(leaf).Score.proportionalNotationDuration = "#1/12"
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)

        >>> abjad.rhythmtrees.extract_trivial_tuplets(voice)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \set Score.proportionalNotationDuration = #1/12
                c'2
            }

    ..  container:: example

        Half-note duration divided ``1:1``:

        >>> string = "(2 (1 1))"
        >>> nodes = abjad.rhythmtrees.parse(string)
        >>> components = abjad.rhythmtrees.call(nodes)
        >>> voice = abjad.Voice(components)
        >>> leaf = abjad.select.leaf(voice, 0)
        >>> abjad.setting(leaf).Score.proportionalNotationDuration = "#1/12"
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    \set Score.proportionalNotationDuration = #1/12
                    c'4
                    c'4
                }
            }

        >>> abjad.rhythmtrees.extract_trivial_tuplets(voice)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \set Score.proportionalNotationDuration = #1/12
                c'4
                c'4
            }

    ..  container:: example

        Half-note duration divided ``1:2``:

        >>> string = "(2 (1 2))"
        >>> nodes = abjad.rhythmtrees.parse(string)
        >>> components = abjad.rhythmtrees.call(nodes)
        >>> voice = abjad.Voice(components)
        >>> leaf = abjad.select.leaf(voice, 0)
        >>> abjad.setting(leaf).Score.proportionalNotationDuration = "#1/12"
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \tuplet 3/2
                {
                    \set Score.proportionalNotationDuration = #1/12
                    c'4
                    c'2
                }
            }

    ..  container:: example

        Successive quarter-note durations, divided ``1``, ``1:1``, ``1:2``:

        >>> string = "(1 (1)) (1 (1 1)) (1 (1 2))"
        >>> nodes = abjad.rhythmtrees.parse(string)
        >>> components = abjad.rhythmtrees.call(nodes)
        >>> voice = abjad.Voice(components)
        >>> leaf = abjad.select.leaf(voice, 0)
        >>> abjad.setting(leaf).Score.proportionalNotationDuration = "#1/12"
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    \set Score.proportionalNotationDuration = #1/12
                    c'4
                }
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'8
                    c'8
                }
                \tuplet 3/2
                {
                    c'8
                    c'4
                }
            }

        >>> abjad.rhythmtrees.extract_trivial_tuplets(voice)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \set Score.proportionalNotationDuration = #1/12
                c'4
                c'8
                c'8
                \tuplet 3/2
                {
                    c'8
                    c'4
                }
            }

    ..  container:: example

        Dyadic durations:

        >>> nodes = abjad.rhythmtrees.parse("1 1/2 1/2 3/2 1/4")
        >>> components = abjad.rhythmtrees.call(nodes)
        >>> voice = abjad.Voice(components)
        >>> abjad.setting(voice[0]).Score.proportionalNotationDuration = "#1/12"
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \set Score.proportionalNotationDuration = #1/12
                c'4
                c'8
                c'8
                c'4.
                c'16
            }

    ..  container:: example

        Tuplets without dotted values:

        >>> string = "(1 (1 (1 (1 1)) 1))"
        >>> nodes = abjad.rhythmtrees.parse(string)
        >>> components = abjad.rhythmtrees.call(nodes, abjad.Duration(1, 2))
        >>> voice = abjad.Voice(components)
        >>> leaf = abjad.select.leaf(voice, 0)
        >>> abjad.setting(leaf).Score.proportionalNotationDuration = "#1/12"
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \tuplet 3/2
                {
                    \set Score.proportionalNotationDuration = #1/12
                    c'4
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 1/1
                    {
                        c'8
                        c'8
                    }
                    c'4
                }
            }

        >>> abjad.rhythmtrees.extract_trivial_tuplets(voice)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \tuplet 3/2
                {
                    \set Score.proportionalNotationDuration = #1/12
                    c'4
                    c'8
                    c'8
                    c'4
                }
            }

    """
    parser = RhythmTreeParser()
    nodes = parser(string)
    assert all(isinstance(_, RhythmTreeContainer | RhythmTreeLeaf) for _ in nodes)
    return nodes


def extract_trivial_tuplets(argument) -> None:
    """
    Extracts trivial tuplets from ``argument``.
    """
    for tuplet in _select.tuplets(argument):
        if tuplet.trivial():
            _mutate.extract(tuplet)
