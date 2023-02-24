"""
Tools for modeling IRCAM-style rhythm trees.
"""
import fractions

import uqbar.containers
import uqbar.graphs

from . import duration as _duration
from . import makers as _makers
from . import math as _math
from . import mutate as _mutate
from . import score as _score
from . import sequence as _sequence
from . import spanners as _spanners
from .parsers.base import Parser


class RhythmTreeMixin:
    """
    Abstract rhythm-tree node.
    """

    ### CLASS VARIABLES ###

    _is_abstract = True

    _state_flag_names: tuple[str, ...] = ("_offsets_are_current",)

    ### INITIALIZER ###

    def __init__(self, preprolated_duration=_duration.Duration(1)):
        self._duration = 0
        self._offset = _duration.Offset(0)
        self._offsets_are_current = False
        self.preprolated_duration = preprolated_duration

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
                    # current_offset += child.duration
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
    def duration(self) -> _duration.Duration | tuple[int, int]:
        """
        Gets node duration.

        ..  container:: example

            >>> string = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> tree = abjad.rhythmtrees.RhythmTreeParser()(string)[0]

            >>> tree.duration
            Duration(1, 1)

            >>> tree[1].duration
            Duration(1, 2)

            >>> tree[1][1].duration
            Duration(1, 4)

        """
        # return self.prolation * self.preprolated_duration
        # return self.prolation * _duration.Duration(self.preprolated_duration)
        if isinstance(self.preprolated_duration, tuple):
            n = self.prolation.numerator * self.preprolated_duration[0]
            d = self.prolation.denominator * self.preprolated_duration[1]
            pair = (n, d)
            return pair
        else:
            assert isinstance(self.preprolated_duration, _duration.Duration)
            duration = self.prolation * self.preprolated_duration
            return duration

    @property
    def pair(self) -> tuple[int, int]:
        """
        Gets preprolated duration as pair.
        """
        if isinstance(self.preprolated_duration, tuple):
            pair = self.preprolated_duration
        else:
            assert isinstance(self.preprolated_duration, _duration.Duration)
            pair = self.preprolated_duration.pair
        return pair

    @property
    def parentage_ratios(self):
        """
        A sequence describing the relative durations of the nodes in a node's improper
        parentage.

        The first item in the sequence is the preprolated_duration of the root node, and
        subsequent items are pairs of the preprolated duration of the next node in the
        parentage and the total preprolated_duration of that node and its siblings:

        ..  container:: example

            >>> a = abjad.rhythmtrees.RhythmTreeContainer(preprolated_duration=abjad.Duration(1))
            >>> b = abjad.rhythmtrees.RhythmTreeContainer(preprolated_duration=abjad.Duration(2))
            >>> c = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=abjad.Duration(3))
            >>> d = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=abjad.Duration(4))
            >>> e = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=abjad.Duration(5))

            >>> a.extend([b, c])
            >>> b.extend([d, e])

            >>> a.parentage_ratios
            (Duration(1, 1),)

            >>> for item in b.parentage_ratios:
            ...     item
            Duration(1, 1)
            (Duration(2, 1), Duration(5, 1))

            >>> for item in c.parentage_ratios:
            ...     item
            Duration(1, 1)
            (Duration(3, 1), Duration(5, 1))

            >>> for item in d.parentage_ratios:
            ...     item
            Duration(1, 1)
            (Duration(2, 1), Duration(5, 1))
            (Duration(4, 1), Duration(9, 1))

            >>> for item in e.parentage_ratios:
            ...     item
            Duration(1, 1)
            (Duration(2, 1), Duration(5, 1))
            (Duration(5, 1), Duration(9, 1))

        Returns tuple.
        """
        result = []
        node = self
        while node.parent is not None:
            result.append(
                (
                    node.preprolated_duration,
                    node.parent._get_contents_duration(),
                )
            )
            node = node.parent
        result.append(node.preprolated_duration)
        return tuple(reversed(result))

    @property
    def preprolated_duration(self) -> _duration.Duration:
        """
        Gets node duration in pulses.

        ..  container:: example

            >>> node = abjad.rhythmtrees.RhythmTreeLeaf(abjad.Duration(1))
            >>> node.preprolated_duration
            Duration(1, 1)

            >>> node.preprolated_duration = abjad.Duration(2)
            >>> node.preprolated_duration
            Duration(2, 1)

            >>> node = abjad.rhythmtrees.RhythmTreeLeaf((2, 4))
            >>> node.preprolated_duration
            (2, 4)

        """
        return self._duration

    @preprolated_duration.setter
    def preprolated_duration(self, argument):
        assert isinstance(argument, tuple | _duration.Duration), repr(argument)
        if isinstance(argument, tuple):
            argument = argument
            assert 0 < fractions.Fraction(*argument)
        else:
            assert isinstance(argument, _duration.Duration)
            assert 0 < argument
        self._duration = argument
        self._mark_entire_tree_for_later_update()

    @property
    def pretty_rtm_format(self):
        """
        Gets pretty-printed RTM format of node.

        ..  container:: example

            >>> string = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> tree = abjad.rhythmtrees.RhythmTreeParser()(string)[0]
            >>> print(tree.pretty_rtm_format)
            (1 (
                (1 (
                    1
                    1))
                (1 (
                    1
                    1))))

        Returns string.
        """
        return "\n".join(self._pretty_rtm_format_pieces())

    @property
    def prolation(self) -> fractions.Fraction:
        """
        Gets node prolation.
        """
        return _math.cumulative_products(self.prolations)[-1]

    @property
    def prolations(self):
        """
        Prolations of rhythm tree node.
        """
        prolations = [fractions.Fraction(1)]
        pairs = _sequence.nwise(self.parentage)
        for child, parent in pairs:
            multiplier = fractions.Fraction(
                _duration.Duration(parent.preprolated_duration),
                parent._get_contents_duration(),
            )
            prolations.append(multiplier)
        return tuple(prolations)

    @property
    def start_offset(self) -> _duration.Offset:
        """
        Gets node start offset.

        ..  container:: example

            >>> string = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> tree = abjad.rhythmtrees.RhythmTreeParser()(string)[0]

            >>> tree.start_offset
            Offset((0, 1))

            >>> tree[1].start_offset
            Offset((1, 2))

            >>> tree[0][1].start_offset
            Offset((1, 4))

        """
        self._update_offsets_of_entire_tree_if_necessary()
        return self._offset

    @property
    def stop_offset(self) -> _duration.Offset:
        """
        Gets node stop offset.
        """
        # return self.start_offset + self.duration
        return self.start_offset + _duration.Duration(self.duration)


class RhythmTreeLeaf(RhythmTreeMixin, uqbar.containers.UniqueTreeNode):
    """
    Rhythm-tree leaf.

    ..  container:: example

        Pitched rhythm-tree leaf makes notes:

        >>> leaf = abjad.rhythmtrees.RhythmTreeLeaf(
        ...     preprolated_duration=abjad.Duration(5), is_pitched=True
        ... )

        >>> leaf((1, 8))
        [Note("c'2"), Note("c'8")]

    ..  container:: example

        Unpitched rhythm-tree leaf makes rests:

        >>> leaf = abjad.rhythmtrees.RhythmTreeLeaf(
        ...     preprolated_duration=abjad.Duration(7), is_pitched=False
        ... )
        >>> leaf((1, 16))
        [Rest('r4..')]

    """

    def __init__(
        self, preprolated_duration=_duration.Duration(1), is_pitched=True, name=None
    ):
        uqbar.containers.UniqueTreeNode.__init__(self, name=name)
        RhythmTreeMixin.__init__(self, preprolated_duration=preprolated_duration)
        self.is_pitched = is_pitched

    def __call__(self, pulse_duration) -> list[_score.Leaf | _score.Tuplet]:
        """
        Makes list of leaves and / or tuplets equal to ``pulse_duration``.
        """
        pulse_duration = _duration.Duration(pulse_duration)
        total_duration = pulse_duration * self.preprolated_duration
        if self.is_pitched:
            return _makers.make_leaves(0, total_duration)
        return _makers.make_leaves([None], total_duration)

    def __graph__(self, **keywords) -> uqbar.graphs.Graph:
        """
        Gets Graphviz graph of rhythm tree leaf.
        """
        graph = uqbar.graphs.Graph(name="G")
        node = uqbar.graphs.Node(
            attributes={"label": str(self.preprolated_duration), "shape": "box"}
        )
        graph.append(node)
        return graph

    def __repr__(self) -> str:
        """
        Gets interpreter representation of rhythm-tree leaf.
        """
        properties = [
            f"preprolated_duration={self.preprolated_duration!r}",
            f"is_pitched={self.is_pitched!r}",
        ]
        if self.name is not None:
            properties.append(f"name={self.name!r}")
        properties_string = ", ".join(properties)
        return f"{type(self).__name__}({properties_string})"

    def _pretty_rtm_format_pieces(self):
        # return [str(self.preprolated_duration)]
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
        Gets RTM format of rhythm tree leaf.

        ..  container:: example

            >>> abjad.rhythmtrees.RhythmTreeLeaf(abjad.Duration(1), is_pitched=True).rtm_format
            '1'
            >>> abjad.rhythmtrees.RhythmTreeLeaf(abjad.Duration(5), is_pitched=False).rtm_format
            '-5'

        """
        string = self._get_fraction_string()
        if self.is_pitched:
            return f"{string!s}"
        return f"-{string!s}"


class RhythmTreeContainer(RhythmTreeMixin, uqbar.containers.UniqueTreeList):
    r"""
    Rhythm-tree container.

    ..  container:: example

        Initializes rhythm-tree container:

        >>> container = abjad.rhythmtrees.RhythmTreeContainer(
        ...     preprolated_duration=abjad.Duration(1),
        ...     children=[],
        ... )
        >>> container
        RhythmTreeContainer((1, 1))

    ..  container:: example

        Similar to Abjad containers, ``RhythmTreeContainer`` supports a list interface,
        and can be appended, extended, indexed and so forth by other ``RhythmTreeMixin``
        subclasses:

        >>> leaf_a = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=abjad.Duration(1))
        >>> leaf_b = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=abjad.Duration(2))
        >>> container.extend([leaf_a, leaf_b])
        >>> for _ in container: _
        RhythmTreeLeaf(preprolated_duration=Duration(1, 1), is_pitched=True)
        RhythmTreeLeaf(preprolated_duration=Duration(2, 1), is_pitched=True)

        >>> another_container = abjad.rhythmtrees.RhythmTreeContainer(
        ...     preprolated_duration=abjad.Duration(2))
        >>> another_container.append(
        ...     abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=abjad.Duration(3)))
        >>> another_container.append(container[1])
        >>> container.append(another_container)
        >>> for _ in container: _
        RhythmTreeLeaf(preprolated_duration=Duration(1, 1), is_pitched=True)
        RhythmTreeContainer((2, 3))

    ..  container:: example

        Call ``RhythmTreeContainer`` with a duration to make tuplets:

        >>> components = container((1, 4))
        >>> tuplet = components[0]
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \times 2/3
            {
                c'8
                \times 4/5
                {
                    c'8.
                    c'8
                }
            }

    """

    ### INITIALIZER ###

    def __init__(
        self, children=None, preprolated_duration=_duration.Duration(1), name=None
    ):
        uqbar.containers.UniqueTreeList.__init__(self, name=name)
        RhythmTreeMixin.__init__(self, preprolated_duration=preprolated_duration)
        if isinstance(children, list | str | tuple):
            self.extend(children)
        elif children is not None:
            raise ValueError(f"can not instantiate {type(self)} with {children!r}.")

    ### SPECIAL METHODS ###

    def __add__(self, argument) -> "RhythmTreeContainer":
        r"""
        Concatenate containers self and argument. The operation c = a + b returns a new
        RhythmTreeContainer c with the content of both a and b, and a
        preprolated_duration equal to the sum of the durations of a and b. The operation
        is non-commutative: the content of the first operand will be placed before the
        content of the second operand:

        ..  container:: example

            >>> a = abjad.rhythmtrees.RhythmTreeParser()('(1 (1 1 1))')[0]
            >>> b = abjad.rhythmtrees.RhythmTreeParser()('(2 (3 4))')[0]
            >>> c = a + b
            >>> c.preprolated_duration
            Duration(3, 1)

            >>> for _ in c: _
            RhythmTreeLeaf(preprolated_duration=Duration(1, 1), is_pitched=True)
            RhythmTreeLeaf(preprolated_duration=Duration(1, 1), is_pitched=True)
            RhythmTreeLeaf(preprolated_duration=Duration(1, 1), is_pitched=True)
            RhythmTreeLeaf(preprolated_duration=Duration(3, 1), is_pitched=True)
            RhythmTreeLeaf(preprolated_duration=Duration(4, 1), is_pitched=True)

        """
        if isinstance(argument, str):
            argument = RhythmTreeParser()(argument)
            assert 1 == len(argument) and isinstance(argument[0], type(self))
            argument = argument[0]
        container = type(self)(
            preprolated_duration=self.preprolated_duration
            + argument.preprolated_duration
        )
        container.extend(self[:])
        container.extend(argument[:])
        return container

    def __call__(self, pulse_duration) -> list[_score.Leaf | _score.Tuplet]:
        r"""
        Makes list of leaves and /or tuplets equal to ``pulse_duration``.

        ..  container:: example

            >>> string = '(1 (1 (2 (1 1 1)) 2))'
            >>> tree = abjad.rhythmtrees.RhythmTreeParser()(string)[0]

            >>> components = tree((1, 4))
            >>> components
            [Tuplet('5:4', "c'16 { 2/3 c'16 c'16 c'16 } c'8")]

            >>> staff = abjad.Staff(components)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \times 4/5
                    {
                        c'16
                        \times 2/3
                        {
                            c'16
                            c'16
                            c'16
                        }
                        c'8
                    }
                }

        """

        def recurse(node, tuplet_duration):
            basic_prolated_duration = tuplet_duration / node._get_contents_duration()
            basic_written_duration = _duration.Duration(
                basic_prolated_duration
            ).equal_or_greater_power_of_two
            tuplet = _score.Tuplet((1, 1), [])
            for child in node.children:
                if isinstance(child, type(self)):
                    tuplet.extend(
                        recurse(
                            child,
                            child.preprolated_duration * basic_written_duration,
                        )
                    )
                else:
                    leaves = child(basic_written_duration)
                    tuplet.extend(leaves)
                    if 1 < len(leaves):
                        _spanners.tie(leaves)
            assert fractions.Fraction(*tuplet.multiplier) == 1, repr(tuplet.multiplier)
            contents_duration = tuplet._get_duration()
            target_duration = tuplet_duration
            multiplier = target_duration / contents_duration
            tuplet.multiplier = _duration.pair(multiplier)
            if fractions.Fraction(*tuplet.multiplier) == 1:
                return tuplet[:]
            return [tuplet]

        pulse_duration = _duration.Duration(pulse_duration)
        assert 0 < pulse_duration
        result = recurse(
            self, pulse_duration * _duration.Duration(self.preprolated_duration)
        )
        for component in result[:]:
            if isinstance(component, _score.Tuplet):
                if component.trivial():
                    _mutate._extract(component)
        return result

    def __graph__(self, **keywords) -> uqbar.graphs.Graph:
        r"""
        Graphs rhythm-tree container.

        ..  container:: example

            >>> string = '(1 (1 (2 (1 1 1)) 2))'
            >>> tree = abjad.rhythmtrees.RhythmTreeParser()(string)[0]
            >>> graph = tree.__graph__()
            >>> print(format(graph, "graphviz"))
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

            >>> abjad.graph(graph) # doctest: +SKIP

        """
        graph = uqbar.graphs.Graph(
            name="G", attributes={"bgcolor": "transparent", "truecolor": True}
        )
        node_mapping = {}
        nodes = [self]
        nodes.extend(self.depth_first())
        for node in nodes:
            graphviz_node = uqbar.graphs.Node()
            graphviz_node.attributes["label"] = str(node.preprolated_duration)
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

    def __radd__(self, argument) -> "RhythmTreeContainer":
        """
        Concatenates containers argument and self.
        """
        assert isinstance(argument, type(self))
        return argument.__add__(self)

    def __repr__(self) -> str:
        """
        Gets interpreter representation of rhythm-tree container.
        """
        class_name = type(self).__name__
        # numerator, denominator = self.duration.pair
        if isinstance(self.duration, tuple):
            numerator, denominator = self.duration
        else:
            assert isinstance(self.duration, _duration.Duration)
            numerator, denominator = self.duration.pair
        return f"{class_name}(({numerator}, {denominator}))"

    ### PRIVATE METHODS ###

    def _get_contents_duration(self) -> _duration.Duration:
        result = sum([_duration.Duration(_.preprolated_duration) for _ in self])
        result = _duration.Duration(result)
        return result

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
        Gets rhythm-tree container RTM format.

        ..  container:: example

            >>> string = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> tree = abjad.rhythmtrees.RhythmTreeParser()(string)[0]
            >>> tree.rtm_format
            '(1 ((1 (1 1)) (1 (1 1))))'

        """
        string = " ".join([x.rtm_format for x in self])
        fraction_string = self._get_fraction_string()
        return f"({fraction_string} ({string}))"


class RhythmTreeParser(Parser):
    r"""
    Rhythm-tree parser.

    ..  container:: example

        Abjad’s rhythm-tree parser parses a micro-language resembling Ircam’s
        RTM Lisp syntax, and generates a sequence of rhythm-tree structures.
        Composers can maniuplate these structures and then convert them to
        Abjad score components.

        >>> parser = abjad.rhythmtrees.RhythmTreeParser()
        >>> string = '(3 (1 (1 ((2 (1 1 1)) 2 2 1))))'
        >>> rhythm_tree_list = parser(string)
        >>> rhythm_tree_container = rhythm_tree_list[0]
        >>> rhythm_tree_container.rtm_format
        '(3 (1 (1 ((2 (1 1 1)) 2 2 1))))'

        >>> for _ in rhythm_tree_container: _
        RhythmTreeLeaf(preprolated_duration=Duration(1, 1), is_pitched=True)
        RhythmTreeContainer((3, 2))

        >>> base_duration = (1, 4)
        >>> component_list = rhythm_tree_container(base_duration)
        >>> tuplet = component_list[0]
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 3/4
            {
                c'2
                \times 4/7
                {
                    \times 2/3
                    {
                        c'8
                        c'8
                        c'8
                    }
                    c'4
                    c'4
                    c'8
                }
            }

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
        prototype = (tuple, _duration.Duration)
        assert isinstance(p[2], prototype), repr(p[2])
        if isinstance(p[2], tuple):
            argument = p[2]
        else:
            assert isinstance(p[2], _duration.Duration)
            argument = p[2]
        assert isinstance(argument, tuple | _duration.Duration)
        p[0] = RhythmTreeContainer(children=p[3], preprolated_duration=argument)

    def p_error(self, p):
        if p:
            print(("Syntax error at '%s'" % p.value))
        else:
            print("Syntax error at EOF")

    def p_leaf__INTEGER(self, p):
        """
        leaf : DURATION
        """
        p[0] = RhythmTreeLeaf(preprolated_duration=abs(p[1]), is_pitched=0 < p[1])

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


def parse_rtm_syntax(string: str) -> _score.Container | _score.Leaf | _score.Tuplet:
    r"""
    Creates rhythm tree from RTM ``string``; then calls rhythm tree on
    quarter-note pulse duration.

    A single quarter note:

    ..  container:: example

        >>> result = abjad.rhythmtrees.parse_rtm_syntax("1")
        >>> result
        Note("c'4")

        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            c'4

        A series of quarter notes:

        >>> result = abjad.rhythmtrees.parse_rtm_syntax("1 1 1 1 1 1")
        >>> result
        Container("c'4 c'4 c'4 c'4 c'4 c'4")

        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            {
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
            }

        Notes with durations of the form ``n * 1/4``:

        >>> result = abjad.rhythmtrees.parse_rtm_syntax("1 2 3 4 5")
        >>> result
        Container("c'4 c'2 c'2. c'1 c'1 c'4")

        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            {
                c'4
                c'2
                c'2.
                c'1
                c'1
                ~
                c'4
            }

        Notes with durations of the form ``1/n * 1/4``:

        >>> result = abjad.rhythmtrees.parse_rtm_syntax("1 1/2 1/3 1/4 1/5")
        >>> result
        Container("c'4 c'8 { 8/12 c'8 } c'16 { 16/20 c'16 }")

        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            {
                c'4
                c'8
                \tweak edge-height #'(0.7 . 0)
                \times 8/12
                {
                    c'8
                }
                c'16
                \tweak edge-height #'(0.7 . 0)
                \times 16/20
                {
                    c'16
                }
            }

        With arbitrary multipliers:

        >>> result = abjad.rhythmtrees.parse_rtm_syntax("1 2/3 3/5")
        >>> result
        Container("c'4 { 4/6 c'4 } { 16/20 c'8. }")

        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            {
                c'4
                \tweak edge-height #'(0.7 . 0)
                \times 4/6
                {
                    c'4
                }
                \tweak edge-height #'(0.7 . 0)
                \times 16/20
                {
                    c'8.
                }
            }

    ..  container:: example

        Divides quarter-note duration into 1 part; results in a note:

        >>> string = "(1 (1))"
        >>> result = abjad.rhythmtrees.parse_rtm_syntax(string)
        >>> result
        Note("c'4")

        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            c'4

        Divides quarter-note duration ``1:1``; results in a container:

        >>> string = "(1 (1 1))"
        >>> result = abjad.rhythmtrees.parse_rtm_syntax(string)
        >>> result
        Container("c'8 c'8")

        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            {
                c'8
                c'8
            }

        Divides quarter-note duration ``1:2``; results in a tuplet:

        >>> string = "(1 (1 2))"
        >>> result = abjad.rhythmtrees.parse_rtm_syntax(string)
        >>> result
        Tuplet('3:2', "c'8 c'4")

        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            \times 2/3
            {
                c'8
                c'4
            }

    ..  container:: example

        Divides half-note duration into 1 part; results in a note:

        >>> string = "(2 (1))"
        >>> result = abjad.rhythmtrees.parse_rtm_syntax(string)
        >>> result
        Note("c'2")

        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            c'2

        Divides half-note duration ``1:1``; results in a container:

        >>> string = "(2 (1 1))"
        >>> result = abjad.rhythmtrees.parse_rtm_syntax(string)
        >>> result
        Container("c'4 c'4")

        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            {
                c'4
                c'4
            }

        Divides half-note duration ``1:2``; results in a tuplet:

        >>> string = "(2 (1 2))"
        >>> result = abjad.rhythmtrees.parse_rtm_syntax(string)
        >>> result
        Tuplet('3:2', "c'4 c'2")

        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            \times 2/3
            {
                c'4
                c'2
            }

    ..  container:: example

        Divides three successive quarter-note durations, according
        to ratios of ``1``, ``1:1``, ``1:2``:

        >>> string = "(1 (1)) (1 (1 1)) (1 (1 2))"
        >>> result = abjad.rhythmtrees.parse_rtm_syntax(string)
        >>> result
        Container("c'4 c'8 c'8 { 2/3 c'8 c'4 }")

        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            {
                c'4
                c'8
                c'8
                \times 2/3
                {
                    c'8
                    c'4
                }
            }

    ..  container:: example

        Another example:

        >>> string = "(1 (1 (1 (1 1)) 1))"
        >>> tuplet = abjad.rhythmtrees.parse_rtm_syntax(string)
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \times 2/3
            {
                c'8
                c'16
                c'16
                c'8
            }

    ..  container:: example

        Fractional durations are allowed:

        >>> string = "(3/4 (1 1/2 (4/3 (1 -1/2 1))))"
        >>> tuplet = abjad.rhythmtrees.parse_rtm_syntax(string)
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 9/17
            {
                c'8
                c'16
                \tweak edge-height #'(0.7 . 0)
                \times 8/15
                {
                    c'8
                    r16
                    c'8
                }
            }

    """
    container = _score.Container()
    rtm_containers = RhythmTreeParser()(string)
    prototype = (RhythmTreeLeaf, RhythmTreeContainer)
    for node in rtm_containers:
        assert isinstance(node, prototype), repr(node)
        components = node((1, 4))
        container.extend(components)
    if len(container) == 1:
        result = container[0]
    else:
        result = container
    prototype_ = (_score.Container, _score.Leaf, _score.Tuplet)
    assert isinstance(result, prototype_), repr(result)
    return result
